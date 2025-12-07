"""Add user accounts for all employees"""
from components.managers.data_manager import DataManager
from datetime import datetime
import hashlib

dm = DataManager()

# Load employees
employees = dm.load_data("employees") or []
print(f"📋 Found {len(employees)} employees\n")

# Load existing users
users = dm.load_data("users") or {}
if not isinstance(users, dict):
    users = {}

# Hash password function (same as AuthManager)
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Default password for all employees
default_password = "password123"
hashed_password = hash_password(default_password)

# Add user accounts for employees who don't have one
added_count = 0
for emp in employees:
    email = emp.get("email")
    name = emp.get("name")
    
    if email and email not in users:
        # Determine role based on position
        position = emp.get("position", "").lower()
        if "manager" in position or "hr manager" in position:
            role = "manager"
        else:
            role = "employee"
        
        users[email] = {
            "password": hashed_password,
            "role": role,
            "name": name,
            "created_at": datetime.now().strftime("%Y-%m-%d"),
            "active": True
        }
        added_count += 1
        print(f"✅ Created user account: {name} ({email}) - Role: {role}")
    else:
        if email in users:
            print(f"⏭️  User account already exists: {name} ({email})")
        else:
            print(f"⚠️  Skipped: {name} - no email address")

# Save users
if added_count > 0:
    dm.save_data("users", users)
    print(f"\n✨ Successfully created {added_count} user accounts!")
    print(f"📊 Total users: {len(users)}")
    print(f"\n🔐 Default password for all new accounts: password123")
else:
    print("\n⚠️  No new user accounts created (all employees already have accounts)")

# Display all users
print(f"\n📋 All user accounts:")
for email, user_data in users.items():
    print(f"   - {user_data.get('name')} ({email}) - Role: {user_data.get('role')}")

