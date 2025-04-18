import subprocess
import json
import shutil
import os
import sys

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

print(check_labels.get("labels"))

if not (any(lambda x: x["name"] == "post") for x in check_labels.get("labels")):
    print("This issue has no labels. Please add a label to the issue and try again.")
    sys.exit(1)

json_string = subprocess.run(
    ["gh", "issue", "view", issue_number, "--json", "title,body"],
    check=True,
    capture_output=True,
).stdout

data = json.loads(json_string)

title = data["title"]

if title.startswith("News: "):
    title = title[6:]

assert (
    title != ""
), "Title not found in issue body. Please ensure the issue body contains a title in the format 'News: <title>' or '<title>'"

data = data["body"].split("###")

date = data[1].strip()

assert (
    date != ""
), "Date not found in issue body. Please ensure the issue body contains a date in the format '### DATE: YYYY-MM-DD'."

if date.startswith("DATE"):
    date = date[5:].strip()

body = data[2].strip()

if body.startswith("Content"):
    body = body[8:].strip()

assert (
    body != ""
), "Body not found in issue body. Please ensure the issue body contains a body in the format '### Content: <body>' or '<body>'"

print(f"Title: {title}")
print(f"Date: {date}")
print(f"Body: {body}")

print("Generating post from issue...")

filename = f"_posts/{date}-news.markdown"

assert not os.path.exists(
    filename
), f"File {filename} already exists. Please delete it or choose a different date."

branch_name = f"issue-{issue_number}"

# Create new branch for issue
subprocess.run(["git", "checkout", "-b", branch_name], check=True)

## make a post in _posts/{data}-news.markdown
with open(filename, "w") as f:
    f.write(f"---\n")
    f.write(f"layout: post\n")
    f.write(f'title: "{title}"\n')
    f.write(f"category: news\n")
    f.write(f"---\n\n")
    f.write(f"{body}\n")

subprocess.run(["git", "add", filename], check=True)

subprocess.run(["git", "commit", "-m", f"Fix #{issue_number}"], check=True)

subprocess.run(
    [
        "git",
        "push",
        "--set-upstream",
        "origin",
        f"issue-{issue_number}",
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
