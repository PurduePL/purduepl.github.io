"""Shared helpers for the issue-to-PR generator scripts."""

import json
import re
import shutil
import subprocess
import sys


def require_gh():
    assert shutil.which("gh") is not None, (
        "GitHub CLI (gh) is not installed. Install from https://cli.github.com/."
    )


def fetch_issue(issue_number, required_label):
    """Verify the issue carries `required_label`; return (title, body)."""
    labels_json = subprocess.run(
        ["gh", "issue", "view", issue_number, "--json", "labels"],
        check=True,
        capture_output=True,
    ).stdout
    labels = json.loads(labels_json).get("labels", [])
    print(f"Labels found: {labels}")
    if not any(label["name"] == required_label for label in labels):
        print(
            f"This issue does not have the {required_label!r} label. "
            "Please add the label and try again."
        )
        sys.exit(1)

    issue_json = subprocess.run(
        ["gh", "issue", "view", issue_number, "--json", "title,body"],
        check=True,
        capture_output=True,
    ).stdout
    issue = json.loads(issue_json)
    return issue["title"], issue["body"]


def strip_html_comments(text):
    """Drop <!-- ... --> comments from a string and trim whitespace."""
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL).strip()


def create_branch(branch_name, reset=False):
    """Check out `branch_name` as a new branch.

    With reset=True, first delete any existing local/remote branch by that name
    (so that re-runs of the issue-edit workflow start clean)."""
    if reset:
        subprocess.run(["git", "branch", "-D", branch_name], capture_output=True)
        subprocess.run(
            ["git", "push", "origin", "--delete", branch_name], capture_output=True
        )
    subprocess.run(["git", "checkout", "-b", branch_name], check=True)


def commit_and_open_pr(paths_to_add, commit_message, branch_name):
    """Stage paths, commit, push, open a PR against master."""
    subprocess.run(["git", "add", *paths_to_add], check=True)
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    subprocess.run(
        ["git", "push", "--set-upstream", "origin", branch_name], check=True
    )
    subprocess.run(
        ["gh", "pr", "create", "--fill", "--base", "master", "--head", branch_name],
        check=True,
    )
