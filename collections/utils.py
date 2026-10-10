"""Shared helpers for the issue-to-PR generator scripts."""

import itertools
import json
import os
import subprocess


def fetch_form(issue_number, *required):
    """Return the issue form's fields as {label: value}, asserting `required` are filled."""
    body = json.loads(
        subprocess.run(
            ["gh", "issue", "view", issue_number, "--json", "body"],
            check=True,
            capture_output=True,
        ).stdout
    )["body"]

    # Issue forms render each field as "### <label>\n\n<value>";
    # bodies written in the browser arrive with CRLF line endings.
    fields = {}
    for section in ("\n" + body.replace("\r\n", "\n")).split("\n### ")[1:]:
        label, _, value = section.partition("\n")
        fields[label.strip()] = value.strip()

    missing = [label for label in required if not fields.get(label)]
    assert not missing, (
        f"Issue body is missing {missing}; found sections {list(fields)}. "
        "Please use the issue form."
    )
    return fields


def commit_and_open_pr(paths, commit_message, branch_name):
    """Commit `paths` to a fresh `branch_name` and open a PR against master.
    Deleting any remote branch by that name first closes its PR, so an edited
    issue regenerates cleanly."""
    subprocess.run(["git", "push", "origin", "--delete", branch_name], capture_output=True)
    for args in (
        ["checkout", "-b", branch_name],
        ["add", *paths],
        ["commit", "-m", commit_message],
        ["push", "origin", branch_name],
    ):
        subprocess.run(["git", *args], check=True)
    subprocess.run(
        ["gh", "pr", "create", "--fill", "--base", "master", "--head", branch_name],
        check=True,
    )


def write_post(date, title, body):
    """Write a news post for `date` under _posts/ and return its path.

    A second post on the same day gets a numbered suffix, as
    2016-08-15-news2.markdown does."""
    path = f"_posts/{date}-news.markdown"
    for n in itertools.count(2):
        if not os.path.exists(path):
            break
        path = f"_posts/{date}-news{n}.markdown"
    with open(path, "w") as f:
        f.write(
            "---\n"
            "layout: post\n"
            f"title: {json.dumps(title)}\n"
            "category: news\n"
            "---\n\n"
            f"{body}\n"
        )
    return path
