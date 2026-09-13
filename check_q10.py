import json
from collections import Counter
with open('listings.json', 'r') as f: listings = json.load(f)
with open('projects.json', 'r') as f: projects = json.load(f)

# count total listings for each project
total_counts = Counter(l.get('project_id') for l in listings if l.get('project_id'))
active_counts = Counter(l.get('project_id') for l in listings if l.get('project_id') and l.get('is_live'))

wrong_projects = []
for p in projects:
    pid = p['project_id']
    claimed = p.get('total_listings', 0)
    actual_total = total_counts.get(pid, 0)
    actual_active = active_counts.get(pid, 0)
    
    # If the doc says it matches what GET /v1/listings returns, and GET /v1/listings returns EVERYTHING (both active and inactive)
    # then it should match `actual_total`. 
    if claimed != actual_total:
        wrong_projects.append((pid, claimed, actual_total, actual_active))

print(f"Number of projects where claimed != actual_total: {len(wrong_projects)}")
for w in wrong_projects[:5]:
    print(f"Project {w[0]}: claimed={w[1]}, total={w[2]}, active={w[3]}")

# What if it matches actual_active?
wrong_active = []
for p in projects:
    if p.get('total_listings', 0) != active_counts.get(p['project_id'], 0):
        wrong_active.append(p['project_id'])
print(f"Number of projects where claimed != active_total: {len(wrong_active)}")
