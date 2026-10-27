#!/usr/bin/env python3
"""Read members.json and write selected columns to a new JSON file."""

import json
from random import randint


INPUT_FILE = "applicants.json"
OUTPUT_FILE = "udu_ward1.json"

REFERENCE_FILE = "personal_details.json"
REFERENCE_OUTPUT_COLUMN = "phone"
REFERENCE_COLUMN_INDEX = 1

COLUMNS = [
    "firstname",
    "lastname",
    "gender",
    "phone",
    "nin",
]


def get_data_rows(rows):
    for item in rows:
        if isinstance(item, dict) and isinstance(item.get("data"), list):
            return item["data"]

    return rows


with open(REFERENCE_FILE, "r", encoding="utf-8") as file:
    reference_rows = get_data_rows(json.load(file))

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    members = json.load(file)

new_members = []

def get_random_polling_unit_id():
    """Returns a random integer between 444448 and 444482 inclusive."""
    return randint(444448, 444482)

for index, member in enumerate(members):
    new_member = {}

    for column in COLUMNS:
        new_member[column] = member.get(column)

    reference_row = reference_rows[index]
    reference_column = list(reference_row.keys())[REFERENCE_COLUMN_INDEX]
    new_member[REFERENCE_OUTPUT_COLUMN] = reference_row[reference_column]

    new_member["stateId"] = 10
    new_member["lgaId"] = 204
    new_member["wardId"] = 2031

    new_member["pollingUnitId"] = get_random_polling_unit_id()

    new_member["password"] = "cbmdelta"
    new_member["role"] = "member"
    new_member["consent"] = True

    new_members.append(new_member)

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(new_members, file, indent=2)

print(f"Wrote {len(new_members)} records to {OUTPUT_FILE}")
