import datetime
import sys

from utils import commit_and_open_pr, fetch_form, write_post

issue_number = sys.argv[1]
fields = fetch_form(issue_number, "Title", "Date", "Content")
date = datetime.date.fromisoformat(fields["Date"]).isoformat()
filename = write_post(date, issue_number, fields["Title"], fields["Content"])
commit_and_open_pr([filename], f"Fix #{issue_number}", f"issue-{issue_number}")
