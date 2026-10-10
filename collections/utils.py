"""Shared helpers for the issue-to-PR generator scripts."""

import json
import subprocess

# Bot filters (Cloudflare's Browser Integrity Check among them) reject the default
# "Python-urllib/x.y" agent by name, so identify the site instead.
USER_AGENT = "purduepl-site-bot/1.0 (+https://purduepl.github.io/)"

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
    """Commit `paths` to a fresh `branch_name` off origin/master and open a PR against it.
    Deleting any remote branch by that name first closes its PR, so an edited
    issue regenerates cleanly."""
    subprocess.run(["git", "push", "origin", "--delete", branch_name], capture_output=True)
    for args in (
        ["checkout", "-b", branch_name, "origin/master"],
        ["add", *paths],
        ["commit", "-m", commit_message],
        ["push", "origin", branch_name],
    ):
        subprocess.run(["git", *args], check=True)
    subprocess.run(
        ["gh", "pr", "create", "--fill", "--base", "master", "--head", branch_name],
        check=True,
    )


def write_post(date, issue_number, title, body):
    """Write the news post for issue `issue_number` under _posts/ and return its path.

    The issue number keeps same-day posts from two PRs, each branched from master,
    out of one path."""
    path = f"_posts/{date}-news-{issue_number}.markdown"
    with open(path, "x") as f:
        f.write(
            "---\n"
            "layout: post\n"
            f"title: {json.dumps(title)}\n"
            "category: news\n"
            "---\n\n"
            f"{body}\n"
        )
    return path
