import json
with open('listings.json', 'r') as f: listings = json.load(f)
fake_ids = ['100-3002878', 'MAG-3000012', 'SQU-3000349', 'MAG-3001311', 'ZER-3000796', 'MAG-3001932', '100-3001372']
for l in listings:
    if l.get('listing_id') in fake_ids:
        print(f"{l['listing_id']} - {l['property_type']} - Bed: {l['bedroom']} - Price: {l['price']}")
        print(f"Desc: {l.get('description')}")
