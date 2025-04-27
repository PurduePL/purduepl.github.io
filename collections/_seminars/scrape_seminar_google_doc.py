#!/usr/bin/env python3
import os
import gspread
import json
from dateutil.parser import *

print(
    "Warning, don't run a script from the internet that you haven't read before... certainly don't give it write permissions - Patrick, August 22, 2023"
)

gc = gspread.service_account()
google_sheet_url = input()
print(google_sheet_url)
sh = gc.open_by_url(google_sheet_url)
print(sh.title)
print(sh.sheet1)

records = sh.sheet1.get_all_records()

print("Asserting some kind of format")
for record in records:
    assert "Date" in record.keys()
    assert "Presenter" in record.keys()
    assert "Title" in record.keys()
    assert "Location" in record.keys()

print("The unfiltered list of records")


def date_filter(x):
    try:
        parse(x["Date"])
        return True
    except ValueError:
        print("Date filtered out:\n", json.dumps(x, indent=2))
        return False


def presenter_filter(x):
    result = x["Presenter"] != "" and x["Presenter"] != "N/A"
    if not result:
        print("Presenter filtered out:\n", json.dumps(x, indent=2))

    return result

def spring_break_filter(x):
    result = x["Location"] != "Bahamas" and x["Title"] != "Spring Break"

    if not result:
        print("Spring break filtered out:\n", json.dumps(x, indent=2))

    return result


print(json.dumps(records, indent=2))
records = filter(date_filter, records)
records = filter(presenter_filter, records)
records = filter(spring_break_filter, records)
""" print(json.dumps(list(records), indent=2)) """
for record in list(records):
    date = parse(record["Date"])
    presenter = record["Presenter"]
    title = record["Title"]
    location = record["Location"]
    file_name = f"{date.year}/{date.year}-{date.month}-{date.day}-seminar.md"
    file_contents = f"""---
layout: post
speaker: "{presenter}"
title: "{title}"
time: 12p EST
location: "{location}"
category: seminar
invited: false
link_abstract: true
bio: "TBA"
---
TBA
"""
    print(file_name)
    print(file_contents)
    if not os.path.exists(file_name):
        open(file_name, mode="w").write(file_contents)
