"""Check performance data for circular references"""
import json

with open('data/performance.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f'Total performance records: {len(data)}')
print(f'Unique employee IDs: {len(set(d.get("employee_id") for d in data))}')

# Check for any non-serializable objects
for i, record in enumerate(data[:5]):
    print(f'\nRecord {i}:')
    for key, value in record.items():
        print(f'  {key}: {type(value).__name__} = {value}')

