#!/usr/bin/env python3
print(
    "Warning, don't run a script from the internet that you haven't read before... certainly don't give it write permissions - Patrick, March 25, 2024"
)

import argparse

parser = argparse.ArgumentParser(description="Generate an email from a seminar file")
parser.add_argument(
    "seminar_file",
    type=argparse.FileType("r"),
    help="The seminar file to generate an email from",
)

args = parser.parse_args()

seminar_info = args.seminar_file.read()

seminar_sections = seminar_info.split("---", maxsplit=2)
assert len(seminar_sections[0]) == 0
abstract = seminar_sections[-1].strip()
seminar_info = "".join(seminar_sections[1:-1])

speaker, title, time, location, bio = None, None, None, None, None
for line in seminar_info.split("\n"):
    if line.startswith("title:"):
        title = line.split(":", maxsplit=1)[1].strip()
    if line.startswith("speaker:"):
        speaker = line.split(":", maxsplit=1)[1].strip()
    if line.startswith("time:"):
        time = line.split(":", maxsplit=1)[1].strip()
    if line.startswith("location:"):
        location = line.split(":", maxsplit=1)[1].strip()
    ## todo Bio does not support multi-line bios
    if line.startswith("bio:"):
        bio = line.split(":", maxsplit=1)[1].strip().strip('"')

assert speaker is not None
assert title is not None
assert time is not None
assert location is not None

speaker = speaker.strip('"')
title = title.strip('"')
location = location.strip('"')

email_title = f"PurPL Seminar: {speaker} - {title}"

email = f"""
Hello All,

{speaker} will be giving the talk at this week's PurPL Seminar.

If you are planning to attend this week, RSVP via the calendar invite so that we can estimate attendance to order food.

Address: {location}
Time: 12:00-1:30 pm (12-12:30 lunch | 12:30-1:30 presentation)

Title:
{title}

Abstract:
{abstract}

Bio:
{bio}

Thanks,
Patrick LaFontaine
"""

print(email_title)
print(email)

food_email = """
Hello,

We have <X> people who signed up for this week's seminar. Please find the details below.

Lunch for <X> / PurPL Seminar
Address: <LOCATION
Contact: <STUDENT CONTACT>

Speaker: <SPEAKER
Title: <TITLE>

RSVPed List:
<PEOPLE>

Thanks,
Patrick
"""

print("\n\n\n\n\n")
print(food_email)
