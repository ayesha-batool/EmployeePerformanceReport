"""Check what's creating performance.json"""
import os
import json
from datetime import datetime

print("Checking performance.json file...")
filepath = "data/performance.json"

if os.path.exists(filepath):
    mtime = os.path.getmtime(filepath)
    mod_time = datetime.fromtimestamp(mtime)
    size = os.path.getsize(filepath)
    
    print(f"✅ File exists")
    print(f"📅 Last modified: {mod_time}")
    print(f"📊 File size: {size} bytes")
    
    if size > 2:  # More than just "[]"
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"📈 Records: {len(data) if isinstance(data, list) else 'N/A'}")
        except:
            print("❌ File is corrupted")
    else:
        print("📝 File is empty (just [])")
else:
    print("❌ File does not exist")

print("\nChecking performances.json file...")
filepath2 = "data/performances.json"
if os.path.exists(filepath2):
    mtime2 = os.path.getmtime(filepath2)
    mod_time2 = datetime.fromtimestamp(mtime2)
    size2 = os.path.getsize(filepath2)
    print(f"✅ File exists")
    print(f"📅 Last modified: {mod_time2}")
    print(f"📊 File size: {size2} bytes")
else:
    print("❌ File does not exist")

