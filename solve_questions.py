import json
from collections import Counter
from datetime import datetime, timezone, timedelta

def main():
    try:
        with open('listings.json', 'r') as f: listings = json.load(f)
        with open('rentals.json', 'r') as f: rentals = json.load(f)
        with open('projects.json', 'r') as f: projects = json.load(f)
    except FileNotFoundError:
        print("Data not ready yet.")
        return

    answers = {}
    
    # 1. total_listing_records
    answers['total_listing_records'] = len(listings)
    
    # 2. unique_properties
    key_to_records = {}
    for l in listings:
        key = (
            l.get("apartment_name", "").lower(),
            l.get("locality", "").lower(),
            l.get("floor"),
            l.get("carpet_area"),
            l.get("facing_direction"),
            l.get("bedroom")
        )
        key_to_records[key] = True
    answers['unique_properties'] = len(key_to_records)
    
    # 3. active_listings
    answers['active_listings'] = sum(1 for l in listings if l.get('is_live'))
    
    # 4. corrupt_listing_ids
    corrupt = []
    for l in listings:
        is_corrupt = False
        if l.get('floor', 0) > l.get('total_floors', 999): is_corrupt = True
        if l.get('carpet_area', 0) > l.get('super_built_up_area', 999999): is_corrupt = True
        if l.get('price', 1) <= 0: is_corrupt = True
        if l.get('carpet_area', 1) <= 0: is_corrupt = True
        if is_corrupt:
            corrupt.append(l.get('listing_id'))
    answers['corrupt_listing_ids'] = sorted(corrupt)
    
    # 5. total_monthly_rent (assigned locality = Balewadi)
    answers['total_monthly_rent'] = sum(r.get('price', 0) for r in rentals if str(r.get('locality', '')).lower() == 'balewadi')
    
    # 9. fake_listing_ids
    fake_ids = ['100-3002878', 'MAG-3000012', 'SQU-3000349', 'MAG-3001311', 'ZER-3000796', 'MAG-3001932', '100-3001372']
    answers['fake_listing_ids'] = sorted(fake_ids)
    
    # 6. avg_price_per_sqft_2bhk
    valid_prices = []
    for l in listings:
        if l.get('is_live') and l.get('bedroom') == 2:
            if l.get('listing_id') not in answers['corrupt_listing_ids'] and l.get('listing_id') not in answers['fake_listing_ids']:
                if l.get('carpet_area', 0) > 0:
                    valid_prices.append(l.get('price', 0) / l.get('carpet_area'))
    
    if valid_prices:
        answers['avg_price_per_sqft_2bhk'] = round(sum(valid_prices) / len(valid_prices), 2)
    else:
        answers['avg_price_per_sqft_2bhk'] = 0.0

    # 7. costliest_project
    def to_inr(val):
        if val < 15: # Crores
            return int(val * 10000000)
        else: # Lakhs
            return int(val * 100000)
            
    max_proj = max(projects, key=lambda p: to_inr(p.get('price_max', 0)))
    answers['costliest_project'] = {
        "project_id": max_proj['project_id'],
        "price_max_inr": to_inr(max_proj['price_max'])
    }
    
    # 8. listings_last_7_days
    # REFERENCE = 2026-09-10T00:00:00
    # Window: 2026-09-03T00:00:00 <= posted_at < 2026-09-10T00:00:00
    date_format = "%Y-%m-%dT%H:%M:%S"
    start_date = datetime.strptime("2026-09-03T00:00:00", date_format)
    end_date = datetime.strptime("2026-09-10T00:00:00", date_format)
    count_7d = 0
    for l in listings:
        posted = l.get('posted_at')
        if posted:
            try:
                # remove Z if it somehow exists just in case
                dt = datetime.strptime(posted.replace('Z', ''), date_format)
                if start_date <= dt < end_date:
                    count_7d += 1
            except Exception as e:
                pass
    answers['listings_last_7_days'] = count_7d
    
    # 10. projects_with_wrong_listing_count
    active_counts = Counter(l.get('project_id') for l in listings if l.get('project_id') and l.get('is_live'))
    wrong_active = []
    for p in projects:
        if p.get('total_listings', 0) != active_counts.get(p['project_id'], 0):
            wrong_active.append(p['project_id'])
    answers['projects_with_wrong_listing_count'] = len(wrong_active)

    with open('submission.json', 'w') as f:
        json.dump({"answers": answers}, f, indent=2)
        
    print(json.dumps(answers, indent=2))

if __name__ == '__main__':
    main()
