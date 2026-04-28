import io
import ipaddress
import json
import os
import re
import socket
import subprocess
import sys
import urllib.parse
import urllib.request

from PIL import Image, ImageOps

from utils import (
    commit_and_open_pr,
    create_branch,
    fetch_issue,
    require_gh,
    strip_html_comments,
)

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


require_gh()
issue_number = sys.argv[1]
title, body = fetch_issue(issue_number, "member")
print(f"Issue title: {title}")

# Extract name from title
name_match = re.search(r"Add member:\s*(.+)", title)
if name_match:
    name = name_match.group(1).strip()
else:
    # Fallback: try to extract from body
    name_section = next(
        (section for section in body.split("###") if "Name" in section), None
    )
    assert name_section is not None, (
        "Name section not found in issue body. Please ensure the issue follows the template format."
    )
    name = strip_html_comments(name_section.replace("Name", ""))

assert name != "" and name != "[Your Name]", (
    "Name not found or is placeholder. Please provide a valid name in the issue title or body."
)

# Parse the body to extract information
sections = body.split("###")

current_status = None
website_link = None
profile_image = None

for section in sections:
    section_clean = section.strip()

    if "Current Status" in section_clean:
        status_content = strip_html_comments(
            section_clean.replace("Current Status", "")
        )
        status_mapping = {
            "alumni": "_alumni",
            "undergraduate": "_undergrads",
            "undergrad": "_undergrads",
            "grad student": "_students",
            "graduate student": "_students",
            "student": "_students",
            "postdoc": "_postdocs",
            "faculty": "_professors",
        }
        for key, folder in status_mapping.items():
            if key.lower() in status_content.lower():
                current_status = folder
                break
        if current_status is None:
            print(f"Status content found: '{status_content}'")
            assert False, (
                f"Could not determine member status from: '{status_content}'. "
                "Please specify one of: Alumni, Undergraduate, Grad Student, Postdoc, Faculty"
            )

    elif "Website Link" in section_clean:
        website_content = strip_html_comments(
            section_clean.replace("Website Link", "")
        )
        url_match = re.search(
            r"(?:https?://)?(?:www\.)?[^\s]+\.[^\s]+", website_content
        )
        if url_match:
            website_link = url_match.group(0)
            print(f"Found URL: {website_link}")

    elif "Profile Image" in section_clean:
        image_content = strip_html_comments(
            section_clean.replace("Profile Image", "")
        )
        if image_content and not image_content.startswith("Please either"):
            profile_image = image_content

assert current_status is not None, (
    "Current Status not found or invalid. Please specify one of: Alumni, Undergraduate, Grad Student, Postdoc, Faculty"
)
assert website_link is not None, (
    "Website Link not found or invalid. Please provide a valid website URL in the issue."
)
assert profile_image is not None, (
    "Profile Image not found or invalid. Please upload an image or provide a URL in the issue."
)

print(f"Name: {name}")
print(f"Status: {current_status}")
print(f"Website: {website_link}")
print(f"Profile Image: {profile_image}")

# Extract a URL from the Profile Image section (markdown, HTML, or bare URL).
downloaded_image_path = None
image_url = None

if profile_image:
    md_match = re.search(r"!\[[^\]]*\]\((\S+?)\)", profile_image)
    if md_match:
        image_url = md_match.group(1)
        print(f"Extracted URL from markdown image: {image_url}")
    elif "<img" in profile_image:
        html_match = re.search(
            r"""<img[^>]+src=["']?([^"'\s>]+)""", profile_image
        )
        if html_match:
            image_url = html_match.group(1)
            print(f"Extracted URL from HTML img tag: {image_url}")
    else:
        candidate = profile_image.strip()
        if candidate.startswith(("http://", "https://")):
            image_url = candidate
            print(f"Using bare URL: {image_url}")

if image_url:
    validate_image_url(image_url)

    image_filename_base = sanitize_name_for_filename(
        name, use_underscores=True, lowercase=True
    )
    image_filename = f"{image_filename_base}.webp"
    assets_path = "../assets/" + image_filename

    try:
        print(f"Downloading image from {image_url}")
        with urllib.request.urlopen(image_url, timeout=30) as resp:
            image_bytes = resp.read(MAX_IMAGE_BYTES + 1)
        assert len(image_bytes) <= MAX_IMAGE_BYTES, (
            f"Image exceeds {MAX_IMAGE_BYTES} bytes; refusing to download."
        )

        with Image.open(io.BytesIO(image_bytes)) as img:
            img.load()
            img = img.convert("RGB")
            img = ImageOps.fit(img, (120, 120), method=Image.Resampling.LANCZOS)
            img.save(assets_path, "WEBP", quality=80, method=6)

        profile_image = f"assets/{image_filename}"
        downloaded_image_path = assets_path
        print(f"Saved 120x120 WebP to {profile_image}")

    except Exception as e:
        assert False, (
            f"Failed to process image from {image_url}: {e}. Please check the URL and try again."
        )
else:
    assert False, (
        "Could not extract a URL from the Profile Image section. Provide one of: "
        "a markdown image `![alt](https://...)`, an HTML `<img src=\"https://...\">`, "
        f"or a plain https:// URL. Got: {profile_image!r}"
    )

filename_base = sanitize_name_for_filename(name, use_underscores=False, lowercase=False)
filename = f"{current_status}/{filename_base}.markdown"

assert not os.path.exists(filename), (
    f"File {filename} already exists. Please delete it or choose a different name."
)

branch_name = f"member-issue-{issue_number}"
print(filename)
print(branch_name)

create_branch(branch_name, reset=True)

with open(filename, "w") as f:
    if current_status == "_professors":
        first_name = name.split()[0] if len(name.split()) > 0 else name
        last_name = " ".join(name.split()[1:]) if len(name.split()) > 1 else ""
        date_str = subprocess.run(
            ["date", "+%Y-%m-%d %H:%M:%S"], capture_output=True, text=True
        ).stdout.strip()

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

paths = [filename]
if downloaded_image_path:
    paths.append(downloaded_image_path)
    print(f"Including image file in PR: {downloaded_image_path}")

commit_and_open_pr(paths, f"Add member {name} - Fix #{issue_number}", branch_name)

print(
    f"Successfully created member file {filename} and opened PR for issue #{issue_number}"
)
