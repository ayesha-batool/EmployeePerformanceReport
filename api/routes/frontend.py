"""
Frontend API Routes - Backend endpoints for Streamlit frontend
All business logic moved here from app.py
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from components.managers.data_manager import DataManager
from components.managers.auth_manager import AuthManager
from components.agents.performance_agent import EnhancedPerformanceAgent
from components.agents.reporting_agent import ReportingAgent
from components.agents.goal_agent import GoalAgent
from components.agents.feedback_agent import FeedbackAgent
from components.agents.notification_agent import NotificationAgent
from components.agents.export_agent import ExportAgent
from components.managers.event_bus import get_event_bus, set_event_bus, EventBus, EventType

router = APIRouter(prefix="/api/frontend", tags=["frontend"])

# Initialize managers and agents (singleton pattern)
_data_manager = None
_auth_manager = None
_agents = None
_event_bus = None

def get_data_manager():
    global _data_manager
    if _data_manager is None:
        _data_manager = DataManager()
    return _data_manager

def get_auth_manager():
    global _auth_manager
    if _auth_manager is None:
        _auth_manager = AuthManager(get_data_manager())
    return _auth_manager

def get_event_bus():
    global _event_bus
    if _event_bus is None:
        _event_bus = EventBus()
        set_event_bus(_event_bus)
    return _event_bus

def get_agents():
    global _agents
    if _agents is None:
        dm = get_data_manager()
        notification_agent = NotificationAgent(dm)
        _agents = {
            "performance_agent": EnhancedPerformanceAgent(dm),
            "reporting_agent": ReportingAgent(dm),
            "goal_agent": GoalAgent(dm, notification_agent),
            "feedback_agent": FeedbackAgent(dm, notification_agent),
            "notification_agent": notification_agent,
            "export_agent": ExportAgent(dm)
        }
    return _agents

# Authentication
class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/auth/login")
async def login(request: LoginRequest):
    """Login endpoint"""
    auth_manager = get_auth_manager()
    result = auth_manager.authenticate(request.email, request.password)
    if result:
        return {"success": True, "user": result}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Goals endpoints
class GoalCreate(BaseModel):
    employee_id: str
    title: str
    description: Optional[str] = ""
    target_value: float = 100
    deadline: str

@router.get("/goals")
async def get_goals(user_id: Optional[str] = None, user_role: str = "employee"):
    """Get goals for user or all goals for managers"""
    agents = get_agents()
    all_goals = agents["goal_agent"].get_all_goals()
    
    if user_role == "employee" and user_id:
        goals = [g for g in all_goals if str(g.get("employee_id", "")) == str(user_id) or str(g.get("user_id", "")) == str(user_id)]
    else:
        goals = all_goals
    
    return {"goals": goals}

@router.post("/goals")
async def create_goal(goal: GoalCreate):
    """Create a new goal"""
    agents = get_agents()
    goal_data = goal.dict()
    result = agents["goal_agent"].create_goal(goal_data)
    if result.get("success"):
        return result
    raise HTTPException(status_code=400, detail=result.get("error", "Failed to create goal"))

# Feedback endpoints
class FeedbackCreate(BaseModel):
    employee_id: str
    given_by: str
    type: str = "general"
    rating: float = 3.0
    content: str

@router.get("/feedback")
async def get_feedback(employee_id: Optional[str] = None, user_role: str = "employee"):
    """Get feedback for employee or all feedback for managers"""
    agents = get_agents()
    
    if user_role == "employee" and employee_id:
        feedbacks = agents["feedback_agent"].get_feedbacks_for_employee(employee_id)
    else:
        feedbacks = agents["feedback_agent"].get_all_feedbacks()
    
    return {"feedbacks": feedbacks}

@router.post("/feedback")
async def create_feedback(feedback: FeedbackCreate):
    """Create new feedback"""
    agents = get_agents()
    feedback_data = feedback.dict()
    result = agents["feedback_agent"].create_feedback(feedback_data)
    if result.get("success"):
        return result
    raise HTTPException(status_code=400, detail=result.get("error", "Failed to create feedback"))

@router.post("/feedback/{feedback_id}/respond")
async def respond_to_feedback(feedback_id: str, response_data: Dict[str, Any]):
    """Respond to feedback"""
    agents = get_agents()
    result = agents["feedback_agent"].respond_to_feedback(feedback_id, response_data)
    if result.get("success"):
        return result
    raise HTTPException(status_code=400, detail=result.get("error", "Failed to respond to feedback"))

# Reports endpoints
@router.get("/reports/overview")
async def get_overview_report():
    """Get overview report"""
    agents = get_agents()
    overview = agents["reporting_agent"].generate_overview_report()
    return overview

@router.get("/reports/project/{project_id}")
async def get_project_report(project_id: str):
    """Get project report"""
    agents = get_agents()
    report = agents["reporting_agent"].generate_project_report(project_id)
    return report

@router.post("/reports/export")
async def export_data(data_type: str):
    """Export data to CSV"""
    agents = get_agents()
    data_manager = get_data_manager()
    data = data_manager.load_data(data_type) or []
    if data:
        result = agents["export_agent"].export_to_csv(data, output_path=f"{data_type}_export.csv")
        return result
    raise HTTPException(status_code=404, detail=f"No {data_type} data to export")

# Employees endpoint
@router.get("/employees")
async def get_employees():
    """Get all employees with performance data"""
    agents = get_agents()
    data_manager = get_data_manager()
    employees = data_manager.load_data("employees") or []
    
    employees_with_performance = []
    for emp in employees:
        eval_data = agents["performance_agent"].evaluate_employee(emp.get("id"), save=False)
        emp_data = emp.copy()
        if eval_data:
            emp_data["performance_score"] = eval_data.get('performance_score', 0)
            emp_data["rank"] = eval_data.get('rank', 'N/A')
        employees_with_performance.append(emp_data)
    
    return {"employees": employees_with_performance}

# Projects and Tasks endpoints
@router.get("/projects")
async def get_projects(user_id: Optional[str] = None, user_role: str = "employee"):
    """Get projects"""
    data_manager = get_data_manager()
    projects = data_manager.load_data("projects") or []
    tasks = data_manager.load_data("tasks") or []
    
    # For employees, filter tasks by assigned_to
    if user_role == "employee" and user_id:
        for project in projects:
            project_tasks = [t for t in tasks if t.get("project_id") == project.get("id") and t.get("assigned_to") == user_id]
            project["tasks"] = project_tasks
    else:
        for project in projects:
            project_tasks = [t for t in tasks if t.get("project_id") == project.get("id")]
            project["tasks"] = project_tasks
    
    return {"projects": projects}

@router.post("/tasks/{task_id}/update")
async def update_task(task_id: str, updates: Dict[str, Any]):
    """Update task"""
    data_manager = get_data_manager()
    tasks = data_manager.load_data("tasks") or []
    
    for task in tasks:
        if str(task.get("id")) == task_id:
            task.update(updates)
            task["updated_at"] = datetime.now().isoformat()
            
            # Publish event
            event_bus = get_event_bus()
            changes = {k: {"old": task.get(k), "new": v} for k, v in updates.items()}
            event_bus.publish_event(EventType.TASK_UPDATED, {"task": task, "changes": changes}, source="api")
            
            if updates.get("status") == "completed":
                event_bus.publish_event(EventType.TASK_COMPLETED, {"task": task}, source="api")
            
            data_manager.save_data("tasks", tasks)
            return {"success": True, "task": task}
    
    raise HTTPException(status_code=404, detail="Task not found")

