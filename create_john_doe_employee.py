"""Create John Doe employee record"""
from components.managers.data_manager import DataManager
from datetime import datetime

dm = DataManager()
employees = dm.load_data("employees") or []

# Check if John Doe already exists
john_exists = any(e.get("email") == "john@company.com" for e in employees)

if not john_exists:
    # Create John Doe employee record
    john_doe = {
        "id": "1",
        "name": "John Doe",
        "email": "john@company.com",
        "department": "Engineering",
        "position": "Software Developer",
        "status": "active",
        "hire_date": "2024-01-15",
        "created_at": datetime.now().isoformat()
    }
    
    employees.append(john_doe)
    dm.save_data("employees", employees)
    print(f"✅ Created employee record for John Doe (ID: {john_doe['id']})")
else:
    print("✅ John Doe employee record already exists")

# Verify
employees = dm.load_data("employees") or []
john = next((e for e in employees if e.get("email") == "john@company.com"), None)
if john:
    print(f"✅ Verified: {john.get('name')} - {john.get('email')} (ID: {john.get('id')})")
else:
    print("❌ John Doe not found after creation")

