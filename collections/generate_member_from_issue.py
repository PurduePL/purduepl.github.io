import subprocess
import json
import shutil
import os
import sys
import re
import urllib.request
import urllib.parse
import io
import ipaddress
import socket

from PIL import Image, ImageOps

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
    """Sanitize a name for use in filenames"""
    # Remove special characters, keep alphanumeric and spaces
    sanitized = re.sub(r"[^a-zA-Z0-9\s]", "", name)

    if use_underscores:
        # Replace spaces with underscores
        sanitized = re.sub(r"\s+", "_", sanitized)
    else:
        # Remove spaces entirely
        sanitized = re.sub(r"\s+", "", sanitized)

    if lowercase:
        sanitized = sanitized.lower()

    return sanitized


assert (
    shutil.which("gh") is not None
), "GitHub CLI (gh) is not installed. Please install it from https://cli.github.com/ and try again."

issue_number = sys.argv[1]

check_labels = json.loads(
    subprocess.run(
        ["gh", "issue", "view", issue_number, "--json", "labels"],
        check=True,
        capture_output=True,
    ).stdout
)

print(f"Labels found: {check_labels.get('labels')}")

if not any(label["name"] == "member" for label in check_labels.get("labels", [])):
    print(
        "This issue does not have the 'member' label. Please add the 'member' label to the issue and try again."
    )
    sys.exit(1)

json_string = subprocess.run(
    ["gh", "issue", "view", issue_number, "--json", "title,body"],
    check=True,
    capture_output=True,
).stdout

data = json.loads(json_string)

title = data["title"]
body = data["body"]

print(f"Issue title: {title}")

# Extract name from title
# TODO: Lets not get it from the body then?
name_match = re.search(r"Add member:\s*(.+)", title)
if name_match:
    name = name_match.group(1).strip()
else:
    # Fallback: try to extract from body
    sections = body.split("###")
    name_section = None
    for section in sections:
        if "Name" in section:
            name_section = section
            break

    assert (
        name_section is not None
    ), "Name section not found in issue body. Please ensure the issue follows the template format."

    # Extract name from the section (remove "Name" and clean up)
    name = name_section.replace("Name", "").strip()
    # Remove HTML comments
    name = re.sub(r"<!--.*?-->", "", name, flags=re.DOTALL).strip()

assert (
    name != "" and name != "[Your Name]"
), "Name not found or is placeholder. Please provide a valid name in the issue title or body."

# Parse the body to extract information
sections = body.split("###")

# Extract Current Status
current_status = None
website_link = None
profile_image = None

for i, section in enumerate(sections):
    section_clean = section.strip()

    if "Current Status" in section_clean:
        # Get the content after "Current Status"
        status_content = section_clean.replace("Current Status", "").strip()
        # Remove HTML comments
        status_content = re.sub(
            r"<!--.*?-->", "", status_content, flags=re.DOTALL
        ).strip()

        # Look for status keywords
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
            assert (
                False
            ), f"Could not determine member status from: '{status_content}'. Please specify one of: Alumni, Undergraduate, Grad Student, Postdoc, Faculty"

    elif "Website Link" in section_clean:
        website_content = section_clean.replace("Website Link", "").strip()
        # Remove HTML comments
        website_content = re.sub(
            r"<!--.*?-->", "", website_content, flags=re.DOTALL
        ).strip()

        # Extract URL - look for any URL pattern
        url_match = re.search(
            r"(?:https?://)?(?:www\.)?[^\s]+\.[^\s]+", website_content
        )
        if url_match:
            website_link = url_match.group(0)
            print(f"Found URL: {website_link}")

    elif "Profile Image" in section_clean:
        image_content = section_clean.replace("Profile Image", "").strip()
        # Remove HTML comments
        image_content = re.sub(
            r"<!--.*?-->", "", image_content, flags=re.DOTALL
        ).strip()

        # Look for uploaded images or URLs
        if image_content and not image_content.startswith("Please either"):
            profile_image = image_content

assert (
    current_status is not None
), "Current Status not found or invalid. Please specify one of: Alumni, Undergraduate, Grad Student, Postdoc, Faculty"

# Require website link
assert (
    website_link is not None
), "Website Link not found or invalid. Please provide a valid website URL in the issue."

# Require profile image
assert (
    profile_image is not None
), "Profile Image not found or invalid. Please upload an image or provide a URL in the issue."

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
        assert (
            False
        ), f"Failed to process image from {image_url}: {e}. Please check the URL and try again."
else:
    assert False, (
        "Could not extract a URL from the Profile Image section. Provide one of: "
        "a markdown image `![alt](https://...)`, an HTML `<img src=\"https://...\">`, "
        f"or a plain https:// URL. Got: {profile_image!r}"
    )

# Create filename from name (sanitize for filesystem)
filename_base = sanitize_name_for_filename(name, use_underscores=False, lowercase=False)
filename = f"{current_status}/{filename_base}.markdown"

assert not os.path.exists(
    filename
), f"File {filename} already exists. Please delete it or choose a different name."

branch_name = f"member-issue-{issue_number}"

print(filename)

print(branch_name)

# Create new branch for issue - first check if it exists and delete it if so
try:
    # Try to delete the branch if it exists (both locally and remotely)
    subprocess.run(["git", "branch", "-D", branch_name], capture_output=True)
    print(f"Deleted existing local branch: {branch_name}")
except subprocess.CalledProcessError:
    # Branch doesn't exist locally, that's fine
    pass

try:
    # Try to delete the remote branch if it exists
    subprocess.run(
        ["git", "push", "origin", "--delete", branch_name], capture_output=True
    )
    print(f"Deleted existing remote branch: {branch_name}")
except subprocess.CalledProcessError:
    # Remote branch doesn't exist, that's fine
    pass

# Now create the new branch
subprocess.run(["git", "checkout", "-b", branch_name], check=True)

# Create the member file
with open(filename, "w") as f:
    if current_status == "_professors":
        # Professors have a more detailed format
        first_name = name.split()[0] if len(name.split()) > 0 else name
        last_name = " ".join(name.split()[1:]) if len(name.split()) > 1 else ""

        f.write(f"---\n")
        f.write(f"layout: post\n")
        f.write(f"title: {json.dumps(name)}\n")
        f.write(f"firstname: {json.dumps(first_name)}\n")
        f.write(f"lastname: {json.dumps(last_name)}\n")
        f.write(f"category: facultycard\n")
        f.write(
            f"date: {subprocess.run(['date', '+%Y-%m-%d %H:%M:%S'], capture_output=True, text=True).stdout.strip()}\n"
        )
        f.write(f"img: {json.dumps(profile_image)}\n")
        f.write(f"href: {json.dumps(website_link)}\n")
        f.write(f"---\n\n")
        f.write(f"<!-- Add research interests and bio here -->\n")
    else:
        # Simpler format for other member types
        f.write(f"---\n")
        f.write(f"title: {json.dumps(name)}\n")
        f.write(f"img: {json.dumps(profile_image)}\n")
        f.write(f"href: {json.dumps(website_link)}\n")
        f.write(f"---\n\n")

subprocess.run(["git", "add", filename], check=True)

# Add downloaded image to git if one was downloaded
if downloaded_image_path:
    subprocess.run(["git", "add", downloaded_image_path], check=True)
    print(f"Added image file to git: {downloaded_image_path}")

subprocess.run(
    ["git", "commit", "-m", f"Add member {name} - Fix #{issue_number}"], check=True
)

subprocess.run(
    [
        "git",
        "push",
        "--set-upstream",
        "origin",
        branch_name,
    ],
    check=True,
)

subprocess.run(
    [
        "gh",
        "pr",
        "create",
        "--fill",
        "--base",
        "master",
        "--head",
        branch_name,
    ],
    check=True,
)

print(
    f"Successfully created member file {filename} and opened PR for issue #{issue_number}"
)
