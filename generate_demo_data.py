"""Generate demo data for empty JSON files"""
import json
import os
from datetime import datetime, timedelta
import random

DATA_DIR = "data"

def generate_projects():
    """Generate demo projects"""
    projects = [
        {
            "id": "1",
            "name": "Website Redesign",
            "description": "Complete redesign of company website with modern UI/UX",
            "status": "active",
            "deadline": (datetime.now() + timedelta(days=45)).isoformat(),
            "manager": "owner@company.com",
            "created_at": (datetime.now() - timedelta(days=30)).isoformat(),
            "updated_at": datetime.now().isoformat()
        },
        {
            "id": "2",
            "name": "Mobile App Development",
            "description": "Develop mobile application for iOS and Android",
            "status": "active",
            "deadline": (datetime.now() + timedelta(days=60)).isoformat(),
            "manager": "owner@company.com",
            "created_at": (datetime.now() - timedelta(days=20)).isoformat(),
            "updated_at": datetime.now().isoformat()
        },
        {
            "id": "3",
            "name": "Database Migration",
            "description": "Migrate legacy database to new cloud infrastructure",
            "status": "in_progress",
            "deadline": (datetime.now() + timedelta(days=30)).isoformat(),
            "manager": "owner@company.com",
            "created_at": (datetime.now() - timedelta(days=15)).isoformat(),
            "updated_at": datetime.now().isoformat()
        },
        {
            "id": "4",
            "name": "API Integration",
            "description": "Integrate third-party APIs for payment processing",
            "status": "active",
            "deadline": (datetime.now() + timedelta(days=25)).isoformat(),
            "manager": "owner@company.com",
            "created_at": (datetime.now() - timedelta(days=10)).isoformat(),
            "updated_at": datetime.now().isoformat()
        },
        {
            "id": "5",
            "name": "Security Audit",
            "description": "Comprehensive security audit and vulnerability assessment",
            "status": "completed",
            "deadline": (datetime.now() - timedelta(days=5)).isoformat(),
            "manager": "owner@company.com",
            "created_at": (datetime.now() - timedelta(days=45)).isoformat(),
            "updated_at": (datetime.now() - timedelta(days=5)).isoformat()
        }
    ]
    return projects

def generate_tasks():
    """Generate demo tasks - assigned to John Doe (employee ID: 1)"""
    tasks = []
    task_titles = [
        "Implement user authentication",
        "Design database schema",
        "Write unit tests",
        "Fix bug in payment module",
        "Update documentation",
        "Code review for PR #123",
        "Setup CI/CD pipeline",
        "Optimize database queries",
        "Create API endpoints",
        "Design user interface mockups",
        "Write integration tests",
        "Deploy to staging environment",
        "Fix responsive design issues",
        "Implement search functionality",
        "Add error logging"
    ]
    
    statuses = ["pending", "in_progress", "completed"]
    priorities = ["low", "medium", "high"]
    
    for i, title in enumerate(task_titles[:10], 1):  # Generate 10 tasks
        status = random.choice(statuses)
        priority = random.choice(priorities)
        
        created_at = datetime.now() - timedelta(days=random.randint(1, 20))
        due_date = datetime.now() + timedelta(days=random.randint(1, 14))
        
        task = {
            "id": str(i),
            "title": title,
            "description": f"Task description for {title}",
            "status": status,
            "priority": priority,
            "assigned_to": "1",  # John Doe's employee ID
            "project_id": str(random.randint(1, 5)),
            "created_at": created_at.isoformat(),
            "due_date": due_date.isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        if status == "completed":
            task["completed_at"] = (created_at + timedelta(days=random.randint(1, 10))).isoformat()
        
        tasks.append(task)
    
    return tasks

def generate_performances():
    """Generate demo performance evaluations"""
    performances = []
    
    # Generate performance data for John Doe (employee ID: 1)
    for i in range(3):  # 3 evaluations
        evaluated_at = datetime.now() - timedelta(days=30 - (i * 10))
        
        performance = {
            "employee_id": "1",  # John Doe
            "performance_score": round(random.uniform(65, 95), 2),
            "completion_rate": round(random.uniform(70, 100), 2),
            "on_time_rate": round(random.uniform(60, 95), 2),
            "total_tasks": random.randint(8, 15),
            "completed_tasks": random.randint(6, 12),
            "average_completion_time": round(random.uniform(2, 7), 2),
            "high_priority_completed": random.randint(2, 5),
            "rank": 1,
            "trend": random.choice(["improving", "stable", "declining"]),
            "evaluated_at": evaluated_at.isoformat()
        }
        performances.append(performance)
    
    return performances

def main():
    """Generate and save demo data for empty files"""
    print("🚀 Generating demo data for empty files...\n")
    
    # Load existing employees to get IDs
    from components.managers.data_manager import DataManager
    dm = DataManager()
    employees = dm.load_data("employees") or []
    
    if not employees:
        print("⚠️ No employees found. Please create employees first.")
        return
    
    print(f"✅ Found {len(employees)} employees")
    
    # Generate data
    projects = generate_projects()
    tasks = generate_tasks()
    performances = generate_performances()
    
    # Save data
    data_files = {
        "projects": projects,
        "tasks": tasks,
        "performances": performances
    }
    
    for filename, data in data_files.items():
        filepath = os.path.join(DATA_DIR, f"{filename}.json")
        current_data = dm.load_data(filename) or []
        
        if len(current_data) == 0:
            dm.save_data(filename, data)
            print(f"✅ Generated {len(data)} {filename}")
        else:
            print(f"⏭️  {filename} already has {len(current_data)} records, skipping")
    
    print(f"\n✨ Demo data generation complete!")
    print(f"📊 Generated data:")
    for filename, data in data_files.items():
        current_data = dm.load_data(filename) or []
        if len(current_data) > 0:
            print(f"   - {filename}: {len(current_data)} records")

if __name__ == "__main__":
    main()

