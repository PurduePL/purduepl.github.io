import json
import os
import re
import sys

from utils import (
    commit_and_open_pr,
    create_branch,
    fetch_issue,
    require_gh,
    strip_html_comments,
)

require_gh()
issue_number = sys.argv[1]
title, body = fetch_issue(issue_number, "news")

if title.startswith("News:"):
    title = title[6:].strip()
if title == "":
    title = "PurPL News!"

sections = body.split("###")

assert len(sections) >= 3, (
    "Issue body is missing required sections. Expected '### DATE' and '### Content' "
    f"headings; found {max(0, len(sections) - 1)} '###' section(s). Please use the News Post template."
)

date = sections[1].strip()
assert date != "", (
    "Date not found in issue body. Please ensure the issue body contains a date "
    "in the format '### DATE: YYYY-MM-DD'."
)
if date.startswith("DATE"):
    date = date[5:].strip()
date = strip_html_comments(date)
date_match = re.search(r"\d{4}-\d{2}-\d{2}", date)
assert date_match, f"Could not find valid date format (YYYY-MM-DD) in: '{date}'"
date = date_match.group(0)

body_text = sections[2].strip()
if body_text.startswith("Content"):
    body_text = body_text[8:].strip()
body_text = strip_html_comments(body_text)
assert body_text != "", (
    "Body not found in issue body. Please ensure the issue body contains a body "
    "in the format '### Content: <body>' or '<body>'"
)

print(f"Title: {title}")
print(f"Date: {date}")
print(f"Body: {body_text}")
print("Generating post from issue...")

filename = f"_posts/{date}-news.markdown"
assert not os.path.exists(filename), (
    f"File {filename} already exists. Please delete it or choose a different date."
)

branch_name = f"issue-{issue_number}"
create_branch(branch_name)

with open(filename, "w") as f:
    f.write("---\n")
    f.write("layout: post\n")
    f.write(f"title: {json.dumps(title)}\n")
    f.write("category: news\n")
    f.write("---\n\n")
    f.write(f"{body_text}\n")

commit_and_open_pr([filename], f"Fix #{issue_number}", branch_name)
