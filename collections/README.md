# PurPL Website Issue Automation

This directory contains scripts that automatically convert GitHub issues into website content.

## News Posts

Create an issue with the "News Post" template → GitHub Actions creates a PR with a new post file.

**Issue format:**

```text
Title: News: <your title>
### DATE
YYYY-MM-DD
### Content
Your content here...
```

## Member Addition

Create an issue with the "Add PurPL member" template → GitHub Actions creates a PR with a new member file.

**Issue format:**

```text
Title: Add member: <Name>
### Name
<Full Name>
### Current Status
<Alumni, Undergraduate, Grad Student, Postdoc, or Faculty>
### Website Link
<URL>
### Profile Image
<Upload or URL>
```

## Manual Usage

```bash
cd collections/
python generate_post_from_issue.py <issue_number>
python generate_member_from_issue.py <issue_number>
```

**Requirements:** GitHub CLI (`gh`), Python 3.x, Git
