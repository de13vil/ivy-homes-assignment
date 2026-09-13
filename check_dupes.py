import json
import collections
from datetime import datetime

with open("listings.json", "r") as f: listings = json.load(f)
with open("rentals.json", "r") as f: rentals = json.load(f)
with open("projects.json", "r") as f: projects = json.load(f)

# Q2
key_to_records = collections.defaultdict(list)
for l in listings:
    key = (
        l.get("apartment_name", "").lower(),
        l.get("locality", "").lower(),
        l.get("floor"),
        l.get("carpet_area"),
        l.get("facing_direction"),
        l.get("bedroom")
    )
    key_to_records[key].append(l)

dupes = {k:v for k,v in key_to_records.items() if len(v) > 1}
for k, records in list(dupes.items()):
    websites = [r.get("website") for r in records]
    print(f"Dup physical: {len(records)} records, websites: {websites}")

print(f"Unique properties: {len(key_to_records)}")
