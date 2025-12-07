"""Verify employees.json file"""
import json
import os

filepath = "data/employees.json"

print("🔍 Checking employees.json file...")
print(f"File exists: {os.path.exists(filepath)}")
print(f"File size: {os.path.getsize(filepath) if os.path.exists(filepath) else 0} bytes")

try:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"Content length: {len(content)} characters")
    print(f"First 200 chars: {content[:200]}")
    
    data = json.loads(content)
    print(f"\n✅ JSON is valid!")
    print(f"Type: {type(data)}")
    print(f"Length: {len(data) if isinstance(data, list) else 'N/A'}")
    
    if isinstance(data, list) and len(data) > 0:
        print(f"\n✅ Employees found: {len(data)}")
        print(f"First employee: {data[0].get('name', 'N/A')} ({data[0].get('email', 'N/A')})")
        john = [e for e in data if e.get('email') == 'john@company.com']
        if john:
            print(f"✅ John Doe found: ID={john[0].get('id')}, Name={john[0].get('name')}")
        else:
            print("❌ John Doe NOT found")
    else:
        print("❌ File is empty or invalid")
        
except json.JSONDecodeError as e:
    print(f"❌ JSON decode error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")

