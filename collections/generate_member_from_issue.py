import datetime
import io
import ipaddress
import json
import os
import re
import socket
import sys
import urllib.parse
import urllib.request

from PIL import Image, ImageOps

from utils import USER_AGENT, commit_and_open_pr, fetch_form

MAX_IMAGE_BYTES = 10 * 1024 * 1024


def validate_image_url(url):
    """Reject non-https URLs and URLs that resolve to non-public IPs (SSRF guard)."""
    parsed = urllib.parse.urlparse(url)
    assert parsed.scheme == "https", f"Image URL must use https://; got: {url!r}"
    assert parsed.hostname, f"Image URL has no hostname: {url!r}"

    hostname = parsed.hostname.lower()
    assert hostname != "localhost" and not hostname.endswith(
        (".local", ".internal", ".localhost")
    ), f"Image URL hostname {hostname!r} looks local/internal."

    try:
        addrinfo = socket.getaddrinfo(parsed.hostname, None)
    except socket.gaierror as e:
        assert False, f"Could not resolve hostname {parsed.hostname!r}: {e}"

    for info in addrinfo:
        ip = ipaddress.ip_address(info[4][0])
        assert not (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_reserved
            or ip.is_multicast
            or ip.is_unspecified
        ), f"Hostname {parsed.hostname!r} resolves to non-public IP {ip}; refusing to fetch."


def sanitize_name_for_filename(name, use_underscores=True, lowercase=True):
    sanitized = re.sub(r"[^a-zA-Z0-9\s]", "", name)
    if use_underscores:
        sanitized = re.sub(r"\s+", "_", sanitized)
    else:
        sanitized = re.sub(r"\s+", "", sanitized)
    if lowercase:
        sanitized = sanitized.lower()
    return sanitized


issue_number = sys.argv[1]
fields = fetch_form(issue_number, "Name", "Current Status", "Website Link", "Profile Image")
name = fields["Name"]
current_status = {
    "Alumni": "_alumni",
    "Undergraduate": "_undergrads",
    "Grad Student": "_students",
    "Postdoc": "_postdocs",
    "Faculty": "_professors",
}[fields["Current Status"]]
website_link = fields["Website Link"]

# Matches a markdown image, an <img src=...>, or a bare URL alike.
url_match = re.search(r"https://[^\s)\"'>]+", fields["Profile Image"])
assert url_match, (
    "Profile Image needs an uploaded image or an https:// URL; "
    f"got {fields['Profile Image']!r}"
)
image_url = url_match.group(0)
validate_image_url(image_url)

image_filename = f"{sanitize_name_for_filename(name)}.webp"
assets_path = f"../assets/{image_filename}"
profile_image = f"assets/{image_filename}"
try:
    print(f"Downloading image from {image_url}")
    req = urllib.request.Request(image_url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        image_bytes = resp.read(MAX_IMAGE_BYTES + 1)
    assert len(image_bytes) <= MAX_IMAGE_BYTES, (
        f"Image exceeds {MAX_IMAGE_BYTES} bytes; refusing to download."
    )
    with Image.open(io.BytesIO(image_bytes)) as img:
        img = ImageOps.fit(img.convert("RGB"), (120, 120), method=Image.Resampling.LANCZOS)
        img.save(assets_path, "WEBP", quality=80, method=6)
except Exception as e:
    assert False, (
        f"Failed to process image from {image_url}: {e}. "
        "If that URL opens fine in a browser, the host is refusing automated "
        "requests; attach the image to the issue instead and re-run."
    )

filename_base = sanitize_name_for_filename(name, use_underscores=False, lowercase=False)
filename = f"{current_status}/{filename_base}.markdown"

assert not os.path.exists(filename), (
    f"File {filename} already exists. Please delete it or choose a different name."
)

with open(filename, "w") as f:
    if current_status == "_professors":
        first_name, _, last_name = name.partition(" ")
        date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        f.write("---\n")
        f.write("layout: post\n")
        f.write(f"title: {json.dumps(name)}\n")
        f.write(f"firstname: {json.dumps(first_name)}\n")
        f.write(f"lastname: {json.dumps(last_name)}\n")
        f.write("category: facultycard\n")
        f.write(f"date: {date_str}\n")
        f.write(f"img: {json.dumps(profile_image)}\n")
        f.write(f"href: {json.dumps(website_link)}\n")
        f.write("---\n\n")
        f.write("<!-- Add research interests and bio here -->\n")
    else:
        f.write("---\n")
        f.write(f"title: {json.dumps(name)}\n")
        f.write(f"img: {json.dumps(profile_image)}\n")
        f.write(f"href: {json.dumps(website_link)}\n")
        f.write("---\n\n")

commit_and_open_pr(
    [filename, assets_path],
    f"Add member {name} - Fix #{issue_number}",
    f"member-issue-{issue_number}",
)

print(
    f"Successfully created member file {filename} and opened PR for issue #{issue_number}"
)
