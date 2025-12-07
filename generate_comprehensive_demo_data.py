"""
Generate comprehensive demo data for all JSON files
"""
import json
import os
from datetime import datetime, timedelta
import random
from components.managers.data_manager import DataManager

DATA_DIR = "data"

def generate_projects():
    """Generate more demo projects"""
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
            "status": "active",
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
        },
        {
            "id": "6",
            "name": "Cloud Infrastructure Setup",
            "description": "Set up cloud infrastructure on AWS",
            "status": "active",
            "deadline": (datetime.now() + timedelta(days=40)).isoformat(),
            "manager": "emily@company.com",
            "created_at": (datetime.now() - timedelta(days=12)).isoformat(),
            "updated_at": datetime.now().isoformat()
        },
        {
            "id": "7",
            "name": "Customer Portal",
            "description": "Build customer self-service portal",
            "status": "active",
            "deadline": (datetime.now() + timedelta(days=50)).isoformat(),
            "manager": "mike@company.com",
            "created_at": (datetime.now() - timedelta(days=8)).isoformat(),
            "updated_at": datetime.now().isoformat()
        },
        {
            "id": "8",
            "name": "Data Analytics Dashboard",
            "description": "Create analytics dashboard for business intelligence",
            "status": "active",
            "deadline": (datetime.now() + timedelta(days=35)).isoformat(),
            "manager": "owner@company.com",
            "created_at": (datetime.now() - timedelta(days=18)).isoformat(),
            "updated_at": datetime.now().isoformat()
        }
    ]
    return projects

def generate_tasks(employees, projects):
    """Generate comprehensive demo tasks"""
    tasks = []
    task_templates = [
        ("Implement user authentication", "high", "completed"),
        ("Design database schema", "high", "in_progress"),
        ("Write unit tests", "medium", "in_progress"),
        ("Fix bug in payment module", "high", "completed"),
        ("Update documentation", "low", "pending"),
        ("Code review for PR #123", "medium", "completed"),
        ("Setup CI/CD pipeline", "high", "in_progress"),
        ("Optimize database queries", "medium", "pending"),
        ("Create API endpoints", "high", "in_progress"),
        ("Design user interface mockups", "medium", "completed"),
        ("Write integration tests", "medium", "in_progress"),
        ("Deploy to staging environment", "high", "pending"),
        ("Fix responsive design issues", "medium", "in_progress"),
        ("Implement search functionality", "high", "completed"),
        ("Add error logging", "low", "completed"),
        ("Setup monitoring and alerts", "medium", "in_progress"),
        ("Refactor legacy code", "low", "pending"),
        ("Create user documentation", "low", "pending"),
        ("Implement caching layer", "medium", "in_progress"),
        ("Performance optimization", "high", "completed"),
        ("Security vulnerability fixes", "high", "completed"),
        ("Add multi-language support", "medium", "pending"),
        ("Create admin dashboard", "high", "in_progress"),
        ("Implement file upload feature", "medium", "completed"),
        ("Setup automated backups", "high", "completed"),
        ("Create REST API documentation", "low", "pending"),
        ("Implement real-time notifications", "high", "in_progress"),
        ("Add data export functionality", "medium", "completed"),
        ("Create mobile responsive design", "high", "in_progress"),
        ("Implement OAuth authentication", "high", "pending")
    ]
    
    for i, (title, priority, status) in enumerate(task_templates, 1):
        # Randomly assign to different employees
        assigned_employee = random.choice(employees) if employees else None
        assigned_to = assigned_employee.get("id") if assigned_employee else "1"
        
        # Randomly assign to projects (some tasks may not have projects)
        project_id = random.choice([None] + [p.get("id") for p in projects]) if projects else None
        
        created_at = datetime.now() - timedelta(days=random.randint(1, 30))
        due_date = datetime.now() + timedelta(days=random.randint(1, 20))
        
        task = {
            "id": str(i),
            "title": title,
            "description": f"Task description for {title}",
            "status": status,
            "priority": priority,
            "assigned_to": assigned_to,
            "project_id": project_id,
            "created_at": created_at.isoformat(),
            "due_date": due_date.isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        if status == "completed":
            task["completed_at"] = (created_at + timedelta(days=random.randint(1, 15))).isoformat()
        
        tasks.append(task)
    
    return tasks

def generate_performances(employees):
    """Generate performance evaluations for all employees"""
    performances = []
    
    for employee in employees:
        emp_id = employee.get("id")
        # Generate 2-4 performance evaluations per employee
        num_evaluations = random.randint(2, 4)
        
        for i in range(num_evaluations):
            evaluated_at = datetime.now() - timedelta(days=random.randint(5, 90))
            
            # Vary performance scores
            base_score = random.uniform(60, 95)
            completion_rate = random.uniform(70, 100)
            on_time_rate = random.uniform(60, 95)
            
            performance = {
                "employee_id": emp_id,
                "performance_score": round(base_score, 2),
                "completion_rate": round(completion_rate, 2),
                "on_time_rate": round(on_time_rate, 2),
                "total_tasks": random.randint(5, 20),
                "completed_tasks": random.randint(4, 18),
                "average_completion_time": round(random.uniform(2, 8), 2),
                "high_priority_completed": random.randint(1, 6),
                "rank": random.randint(1, len(employees)),
                "trend": random.choice(["improving", "stable", "declining"]),
                "evaluated_at": evaluated_at.isoformat()
            }
            performances.append(performance)
    
    return performances

def generate_goals(employees):
    """Generate goals for employees"""
    goals = []
    goal_templates = [
        ("Complete 10 tasks this month", 10, "performance"),
        ("Improve code quality score", 85, "skills"),
        ("Attend 3 training sessions", 3, "development"),
        ("Reduce bug count by 20%", 20, "performance"),
        ("Complete certification course", 1, "skills"),
        ("Lead a project successfully", 1, "leadership"),
        ("Mentor 2 junior developers", 2, "development"),
        ("Improve customer satisfaction score", 90, "performance"),
        ("Complete all assigned tasks on time", 100, "performance"),
        ("Learn new technology stack", 1, "skills")
    ]
    
    goal_id = 1
    for employee in employees:
        emp_id = employee.get("id")
        # Each employee gets 2-4 goals
        num_goals = random.randint(2, 4)
        selected_goals = random.sample(goal_templates, min(num_goals, len(goal_templates)))
        
        for title, target, category in selected_goals:
            current = random.randint(0, target)
            progress = (current / target * 100) if target > 0 else 0
            status = "completed" if progress >= 100 else "active"
            
            deadline = datetime.now() + timedelta(days=random.randint(10, 60))
            
            goal = {
                "id": str(goal_id),
                "employee_id": emp_id,
                "title": title,
                "description": f"Goal: {title}",
                "target_value": target,
                "current_value": current,
                "progress_percentage": round(progress, 2),
                "status": status,
                "deadline": deadline.isoformat(),
                "category": category,
                "created_at": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            goals.append(goal)
            goal_id += 1
    
    return goals

def generate_feedback(employees):
    """Generate feedback for employees"""
    feedback_list = []
    feedback_templates = [
        ("Excellent work on the recent project", "performance", "Great job!"),
        ("Need to improve communication skills", "behavior", "Please work on this"),
        ("Strong technical skills demonstrated", "skills", "Keep it up"),
        ("Timely task completion", "performance", "Well done"),
        ("Could improve time management", "behavior", "Focus on prioritization"),
        ("Outstanding problem-solving abilities", "skills", "Excellent"),
        ("Good collaboration with team", "behavior", "Great teamwork"),
        ("Needs more attention to detail", "performance", "Please review work carefully")
    ]
    
    feedback_id = 1
    for employee in employees:
        emp_id = employee.get("id")
        # Each employee gets 2-5 feedback entries
        num_feedback = random.randint(2, 5)
        selected_feedback = random.sample(feedback_templates, min(num_feedback, len(feedback_templates)))
        
        for title, category, content in selected_feedback:
            created_at = datetime.now() - timedelta(days=random.randint(1, 60))
            
            feedback = {
                "id": str(feedback_id),
                "employee_id": emp_id,
                "title": title,
                "content": content,
                "category": category,
                "status": random.choice(["pending_response", "responded", "closed"]),
                "created_at": created_at.isoformat(),
                "updated_at": created_at.isoformat()
            }
            
            # Some feedback has responses
            if random.random() > 0.5:
                feedback["employee_response"] = "Thank you for the feedback. I will work on this."
                feedback["status"] = "responded"
            
            feedback_list.append(feedback)
            feedback_id += 1
    
    return feedback_list

def generate_notifications(employees):
    """Generate notifications for employees"""
    notifications = []
    notification_templates = [
        ("New Task Assigned", "task_assignment", "You have been assigned a new task"),
        ("Task Completed", "task_completion", "Your task has been marked as completed"),
        ("Feedback Received", "feedback", "You have received new feedback"),
        ("Goal Updated", "goal_update", "Your goal progress has been updated"),
        ("Performance Review", "performance", "Your performance has been evaluated"),
        ("Deadline Approaching", "deadline", "A task deadline is approaching"),
        ("Project Update", "project", "There's an update on your project"),
        ("Achievement Unlocked", "achievement", "Congratulations! You've earned an achievement")
    ]
    
    notification_id = 1
    for employee in employees:
        emp_id = employee.get("id")
        # Each employee gets 5-10 notifications
        num_notifications = random.randint(5, 10)
        
        for i in range(num_notifications):
            title, ntype, message = random.choice(notification_templates)
            created_at = datetime.now() - timedelta(days=random.randint(0, 30))
            
            notification = {
                "id": str(notification_id),
                "recipient": emp_id,
                "title": title,
                "message": f"{message} - {created_at.strftime('%Y-%m-%d')}",
                "notification_type": ntype,
                "read": random.choice([True, False]),
                "created_at": created_at.isoformat()
            }
            
            if notification["read"]:
                notification["read_at"] = (created_at + timedelta(hours=random.randint(1, 24))).isoformat()
            
            notifications.append(notification)
            notification_id += 1
    
    return notifications

def generate_achievements(employees):
    """Generate achievements for employees"""
    achievements = []
    achievement_templates = [
        ("First Task Completed", "task_completion", "low"),
        ("10 Tasks Completed", "task_completion", "medium"),
        ("50 Tasks Completed", "task_completion", "high"),
        ("Perfect Attendance", "attendance", "medium"),
        ("Top Performer", "performance", "high"),
        ("Team Player", "collaboration", "medium"),
        ("Quick Learner", "skills", "low"),
        ("Project Champion", "project", "high")
    ]
    
    achievement_id = 1
    for employee in employees:
        emp_id = employee.get("id")
        # Each employee gets 2-5 achievements
        num_achievements = random.randint(2, 5)
        selected_achievements = random.sample(achievement_templates, min(num_achievements, len(achievement_templates)))
        
        for title, category, impact in selected_achievements:
            created_at = datetime.now() - timedelta(days=random.randint(1, 90))
            
            achievement = {
                "id": str(achievement_id),
                "employee_id": emp_id,
                "title": title,
                "description": f"Achievement: {title}",
                "category": category,
                "impact": impact,
                "created_at": created_at.isoformat()
            }
            achievements.append(achievement)
            achievement_id += 1
    
    return achievements

def generate_risks(employees, projects, tasks):
    """Generate risks for projects and employees"""
    risks = []
    risk_templates = [
        ("High workload detected", "workload", "high"),
        ("Missed deadline", "deadline", "high"),
        ("Low performance", "performance", "medium"),
        ("Resource constraint", "resource", "medium"),
        ("Technical debt", "technical", "low"),
        ("Scope creep", "scope", "medium")
    ]
    
    risk_id = 1
    # Generate project risks
    for project in projects[:3]:  # First 3 projects
        risk_type, category, severity = random.choice(risk_templates)
        risk = {
            "id": str(risk_id),
            "project_id": project.get("id"),
            "type": risk_type,
            "category": category,
            "severity": severity,
            "description": f"Risk identified: {risk_type}",
            "status": "active",
            "created_at": (datetime.now() - timedelta(days=random.randint(1, 10))).isoformat()
        }
        risks.append(risk)
        risk_id += 1
    
    # Generate employee risks
    for employee in employees[:5]:  # First 5 employees
        if random.random() > 0.6:  # 40% chance of risk
            risk_type, category, severity = random.choice(risk_templates)
            risk = {
                "id": str(risk_id),
                "employee_id": employee.get("id"),
                "type": risk_type,
                "category": category,
                "severity": severity,
                "description": f"Risk for {employee.get('name')}: {risk_type}",
                "status": "active",
                "created_at": (datetime.now() - timedelta(days=random.randint(1, 7))).isoformat()
            }
            risks.append(risk)
            risk_id += 1
    
    return risks

def generate_attendance(employees):
    """Generate attendance records for employees"""
    attendance = []
    attendance_id = 1
    
    for employee in employees:
        emp_id = employee.get("id")
        # Generate attendance for last 30 days
        for day in range(30):
            date = datetime.now() - timedelta(days=day)
            # 90% attendance rate
            status = "present" if random.random() > 0.1 else "absent"
            
            if status == "present":
                check_in = date.replace(hour=random.randint(8, 10), minute=random.randint(0, 59))
                check_out = check_in + timedelta(hours=random.randint(7, 9))
                
                attendance_record = {
                    "id": str(attendance_id),
                    "employee_id": emp_id,
                    "date": date.date().isoformat(),
                    "status": status,
                    "check_in_time": check_in.isoformat(),
                    "check_out_time": check_out.isoformat(),
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }
            else:
                attendance_record = {
                    "id": str(attendance_id),
                    "employee_id": emp_id,
                    "date": date.date().isoformat(),
                    "status": status,
                    "check_in_time": None,
                    "check_out_time": None,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }
            
            attendance.append(attendance_record)
            attendance_id += 1
    
    return attendance

def generate_reviews_360(employees):
    """Generate 360° reviews for employees"""
    reviews = []
    review_id = 1
    
    for employee in employees:
        emp_id = employee.get("id")
        # Each employee gets 1-3 reviews
        num_reviews = random.randint(1, 3)
        
        for i in range(num_reviews):
            # Self review
            reviews.append({
                "id": str(review_id),
                "employee_id": emp_id,
                "reviewer_id": emp_id,
                "reviewer_type": "self",
                "rating": round(random.uniform(70, 90), 2),
                "comments": "Self-assessment: Doing well overall",
                "created_at": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat()
            })
            review_id += 1
            
            # Peer review (if there are other employees)
            if len(employees) > 1:
                peer = random.choice([e for e in employees if e.get("id") != emp_id])
                reviews.append({
                    "id": str(review_id),
                    "employee_id": emp_id,
                    "reviewer_id": peer.get("id"),
                    "reviewer_type": "peer",
                    "rating": round(random.uniform(65, 95), 2),
                    "comments": "Good team player, helpful colleague",
                    "created_at": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat()
                })
                review_id += 1
            
            # Manager review
            reviews.append({
                "id": str(review_id),
                "employee_id": emp_id,
                "reviewer_id": "manager@company.com",
                "reviewer_type": "manager",
                "rating": round(random.uniform(70, 95), 2),
                "comments": "Solid performance, meeting expectations",
                "created_at": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat()
            })
            review_id += 1
    
    return reviews

def generate_badges(employees):
    """Generate badges for employees"""
    badges = []
    badge_types = [
        "top_performer",
        "goal_achiever",
        "team_player",
        "on_time_master",
        "feedback_champion",
        "skill_expert",
        "attendance_star"
    ]
    
    badge_id = 1
    for employee in employees:
        emp_id = employee.get("id")
        # Each employee gets 1-3 badges
        num_badges = random.randint(1, 3)
        selected_badges = random.sample(badge_types, min(num_badges, len(badge_types)))
        
        for badge_type in selected_badges:
            badge_names = {
                "top_performer": "⭐ Top Performer",
                "goal_achiever": "🎯 Goal Achiever",
                "team_player": "🏆 Best Team Player",
                "on_time_master": "⏰ On-Time Master",
                "feedback_champion": "💬 Feedback Champion",
                "skill_expert": "🎓 Skill Expert",
                "attendance_star": "📅 Attendance Star"
            }
            
            badge_emojis = {
                "top_performer": "⭐",
                "goal_achiever": "🎯",
                "team_player": "🏆",
                "on_time_master": "⏰",
                "feedback_champion": "💬",
                "skill_expert": "🎓",
                "attendance_star": "📅"
            }
            
            badge = {
                "id": str(badge_id),
                "employee_id": emp_id,
                "badge_type": badge_type,
                "badge_name": badge_names.get(badge_type, "Badge"),
                "badge_emoji": badge_emojis.get(badge_type, "🏅"),
                "reason": f"Earned {badge_names.get(badge_type, 'Badge')} badge",
                "awarded_at": (datetime.now() - timedelta(days=random.randint(1, 60))).isoformat()
            }
            badges.append(badge)
            badge_id += 1
    
    return badges

def add_skills_to_employees(employees):
    """Add skills to employee records"""
    skill_sets = {
        "developer": ["Python", "JavaScript", "React", "Node.js", "SQL", "Git"],
        "designer": ["UI/UX Design", "Figma", "Photoshop", "Illustrator", "Prototyping"],
        "manager": ["Leadership", "Project Management", "Communication", "Strategic Planning"],
        "marketing": ["Digital Marketing", "SEO", "Content Writing", "Analytics", "Social Media"]
    }
    
    for employee in employees:
        position = employee.get("position", "").lower()
        skills = {}
        
        # Assign skills based on position
        if "developer" in position or "engineer" in position:
            selected_skills = random.sample(skill_sets["developer"], random.randint(3, 6))
        elif "design" in position:
            selected_skills = random.sample(skill_sets["designer"], random.randint(3, 5))
        elif "manager" in position:
            selected_skills = random.sample(skill_sets["manager"], random.randint(3, 4))
        else:
            selected_skills = random.sample(skill_sets["marketing"], random.randint(3, 5))
        
        # Assign skill levels (1-5)
        for skill in selected_skills:
            skills[skill] = random.randint(2, 5)
        
        employee["skills"] = skills
    
    return employees

def main():
    """Generate comprehensive demo data"""
    print("🚀 Generating comprehensive demo data...\n")
    
    dm = DataManager()
    
    # Load existing employees
    employees = dm.load_data("employees") or []
    if not employees:
        print("⚠️ No employees found. Please create employees first.")
        return
    
    print(f"✅ Found {len(employees)} employees")
    
    # Add skills to employees
    employees = add_skills_to_employees(employees)
    dm.save_data("employees", employees)
    print(f"✅ Added skills to {len(employees)} employees")
    
    # Generate all data
    projects = generate_projects()
    tasks = generate_tasks(employees, projects)
    performances = generate_performances(employees)
    goals = generate_goals(employees)
    feedback = generate_feedback(employees)
    notifications = generate_notifications(employees)
    achievements = generate_achievements(employees)
    risks = generate_risks(employees, projects, tasks)
    attendance = generate_attendance(employees)
    reviews_360 = generate_reviews_360(employees)
    badges = generate_badges(employees)
    
    # Save all data (append to existing or replace if empty)
    data_files = {
        "projects": projects,
        "tasks": tasks,
        "performances": performances,
        "goals": goals,
        "feedback": feedback,
        "notifications": notifications,
        "achievements": achievements,
        "risks": risks,
        "attendance": attendance,
        "reviews_360": reviews_360,
        "badges": badges
    }
    
    print("\n📊 Generating data files...")
    for filename, data in data_files.items():
        current_data = dm.load_data(filename) or []
        
        if len(current_data) == 0:
            dm.save_data(filename, data)
            print(f"✅ Generated {len(data)} {filename}")
        else:
            # Append new data to existing
            combined = current_data + data
            dm.save_data(filename, combined)
            print(f"✅ Added {len(data)} new {filename} (total: {len(combined)})")
    
    print(f"\n✨ Comprehensive demo data generation complete!")
    print(f"\n📈 Summary:")
    for filename, data in data_files.items():
        final_data = dm.load_data(filename) or []
        print(f"   - {filename}: {len(final_data)} records")

if __name__ == "__main__":
    main()

