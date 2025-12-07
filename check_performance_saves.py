"""Check what's causing performance.json to be saved"""
import json
import os
from datetime import datetime

# Check file modification time
filepath = "data/performance.json"
if os.path.exists(filepath):
    mtime = os.path.getmtime(filepath)
    mod_time = datetime.fromtimestamp(mtime)
    print(f"📅 Last modified: {mod_time}")
    print(f"⏰ Time since modification: {(datetime.now() - mod_time).total_seconds():.1f} seconds ago")
    
    # Check file size
    size = os.path.getsize(filepath)
    print(f"📊 File size: {size:,} bytes")
    
    # Count records
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"📈 Total records: {len(data)}")
        
        # Check most recent
        if data:
            recent = sorted(data, key=lambda x: x.get('evaluated_at', ''), reverse=True)[:3]
            print(f"\n🕐 Most recent 3 evaluations:")
            for r in recent:
                print(f"  - {r.get('evaluated_at')} - Employee {r.get('employee_id')}")
    except Exception as e:
        print(f"❌ Error reading file: {e}")
else:
    print("❌ File does not exist")

