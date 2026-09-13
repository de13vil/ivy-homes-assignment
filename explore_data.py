import json
from collections import Counter
import re

with open("listings.json", "r") as f: listings = json.load(f)
with open("rentals.json", "r") as f: rentals = json.load(f)
with open("projects.json", "r") as f: projects = json.load(f)

print("--- CORRUPT CHECK ---")
for l in listings:
    is_corrupt = False
    reasons = []
    if l.get('floor', 0) > l.get('total_floors', 999): 
        is_corrupt = True
        reasons.append("floor > total_floors")
    if l.get('carpet_area', 0) > l.get('super_built_up_area', 999999):
        is_corrupt = True
        reasons.append("carpet > super")
    if l.get('price', 1) <= 0:
        is_corrupt = True
        reasons.append("price <= 0")
    if l.get('carpet_area', 1) <= 0:
        is_corrupt = True
        reasons.append("carpet <= 0")
    if l.get('bathroom', 0) > l.get('bedroom', 0) + 2: # heuristic
        pass
    if is_corrupt:
        print(f"Corrupt {l['listing_id']}: {reasons}")

print("\n--- FAKE CHECK ---")
for l in listings:
    is_fake = False
    reasons = []
    # dummy phone?
    phone = l.get('posted_by_contact', '')
    if phone == '+910000000000' or len(set(phone[3:])) == 1:
        is_fake = True
        reasons.append(f"fake phone {phone}")
    
    # 1 rupee price?
    if 0 < l.get('price', 0) < 10000:
        is_fake = True
        reasons.append(f"absurd price {l.get('price')}")
        
    if is_fake:
        print(f"Fake {l['listing_id']}: {reasons}")

print("\n--- PROJECT MAX PRICE CHECK ---")
max_p = max(projects, key=lambda p: p.get('price_max', 0))
print(f"Max project: {max_p['project_id']} with max price {max_p.get('price_max')}")

print("\n--- PROJECT COUNT CHECK ---")
proj_counts = Counter(l.get('project_id') for l in listings if l.get('project_id'))
wrong_count = 0
for p in projects:
    pid = p['project_id']
    actual = proj_counts.get(pid, 0)
    if p.get('total_listings') != actual:
        # wait, does the endpoint return active only? The doc said GET /v1/listings returns active sale listings.
        # So maybe total_listings should match active listings?
        active_actual = sum(1 for l in listings if l.get('project_id') == pid and l.get('is_live'))
        if p.get('total_listings') not in (actual, active_actual):
            wrong_count += 1
print(f"Projects with wrong listing count: {wrong_count}")

