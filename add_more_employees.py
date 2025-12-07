"""Add more employees to the system"""
from components.managers.data_manager import DataManager
from datetime import datetime
import random

dm = DataManager()
employees = dm.load_data("employees") or []

# Additional employees to add
new_employees = [
    {
        "id": "2",
        "name": "Jane Smith",
        "email": "jane@company.com",
        "department": "Engineering",
        "position": "Senior Software Developer",
        "status": "active",
        "hire_date": "2023-06-10",
        "created_at": datetime.now().isoformat()
    },
    {
        "id": "3",
        "name": "Mike Johnson",
        "email": "mike@company.com",
        "department": "Marketing",
        "position": "Marketing Manager",
        "status": "active",
        "hire_date": "2023-03-15",
        "created_at": datetime.now().isoformat()
    },
    {
        "id": "4",
        "name": "Sarah Williams",
        "email": "sarah@company.com",
        "department": "Engineering",
        "position": "QA Engineer",
        "status": "active",
        "hire_date": "2024-02-20",
        "created_at": datetime.now().isoformat()
    },
    {
        "id": "5",
        "name": "David Brown",
        "email": "david@company.com",
        "department": "Sales",
        "position": "Sales Representative",
        "status": "active",
        "hire_date": "2023-09-05",
        "created_at": datetime.now().isoformat()
    },
    {
        "id": "6",
        "name": "Emily Davis",
        "email": "emily@company.com",
        "department": "HR",
        "position": "HR Manager",
        "status": "active",
        "hire_date": "2023-01-12",
        "created_at": datetime.now().isoformat()
    },
    {
        "id": "7",
        "name": "Robert Wilson",
        "email": "robert@company.com",
        "department": "Engineering",
        "position": "DevOps Engineer",
        "status": "active",
        "hire_date": "2024-04-18",
        "created_at": datetime.now().isoformat()
    },
    {
        "id": "8",
        "name": "Lisa Anderson",
        "email": "lisa@company.com",
        "department": "Design",
        "position": "UI/UX Designer",
        "status": "active",
        "hire_date": "2023-11-22",
        "created_at": datetime.now().isoformat()
    }
]

# Check which employees already exist
existing_emails = {e.get("email") for e in employees}
existing_ids = {e.get("id") for e in employees}

# Add only new employees
added_count = 0
for emp in new_employees:
    if emp.get("email") not in existing_emails and emp.get("id") not in existing_ids:
        employees.append(emp)
        existing_emails.add(emp.get("email"))
        existing_ids.add(emp.get("id"))
        added_count += 1
        print(f"✅ Added: {emp.get('name')} ({emp.get('email')}) - {emp.get('position')}")
    else:
        print(f"⏭️  Skipped: {emp.get('name')} - already exists")

# Save updated employees list
if added_count > 0:
    dm.save_data("employees", employees)
    print(f"\n✨ Successfully added {added_count} new employees!")
    print(f"📊 Total employees: {len(employees)}")
else:
    print("\n⚠️  No new employees added (all already exist)")

# Display all employees
print(f"\n📋 All employees:")
for emp in employees:
    print(f"   - {emp.get('name')} ({emp.get('email')}) - {emp.get('department')} - {emp.get('position')}")

