#!/usr/bin/env python3
"""Read members.json and write selected columns to a new JSON file."""

import json
from random import randint


INPUT_FILE = "sample_data.json"
OUTPUT_FILE = "patani.json"

COLUMNS = [
    "firstName",
    "lastName",
    "phone",
]


def get_data_rows(rows):
    for item in rows:
        if isinstance(item, dict) and isinstance(item.get("data"), list):
            return item["data"]

    return rows

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    members = json.load(file)

new_members = []

def generate_random_11_digits():
    """
    Generates a random 11-digit number as a string
    ensuring that the first digit is never 0.
    """
    # Generate the first digit (1-9) to ensure it doesn't start with zero
    first_digit = str(randint(1, 9))
    
    # Generate the remaining 10 digits (0-9)
    remaining_digits = "".join(str(randint(0, 9)) for _ in range(10))
    
    return first_digit + remaining_digits

def get_random_polling_unit_id():
    """Returns a random integer between 444448 and 444482 inclusive."""
    return randint(444139, 444145)

for index, member in enumerate(members):
    new_member = {}

    for column in COLUMNS:
        new_member[column] = member.get(column)

    new_member["stateId"] = 10
    new_member["lgaId"] = 194
    new_member["wardId"] = 2014

    new_member["pollingUnitId"] = get_random_polling_unit_id()

    new_member["nin"] = generate_random_11_digits()
    new_member["password"] = "cbmdelta"
    new_member["role"] = "member"
    new_member["consent"] = True

    new_members.append(new_member)

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(new_members, file, indent=2)

print(f"Wrote {len(new_members)} records to {OUTPUT_FILE}")
