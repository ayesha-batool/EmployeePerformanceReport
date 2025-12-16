"""
Dashboard API Routes - Backend endpoints for Streamlit frontend
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, Optional
from pydantic import BaseModel
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from components.managers.data_manager import DataManager
from components.agents.performance_agent import EnhancedPerformanceAgent
from components.agents.reporting_agent import ReportingAgent
from components.agents.goal_agent import GoalAgent
from components.agents.notification_agent import NotificationAgent

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

# Initialize agents (singleton pattern)
_data_manager = None
_agents = None

def get_data_manager():
    global _data_manager
    if _data_manager is None:
        _data_manager = DataManager()
    return _data_manager

def get_agents():
    global _agents
    if _agents is None:
        dm = get_data_manager()
        notification_agent = NotificationAgent(dm)
        _agents = {
            "performance_agent": EnhancedPerformanceAgent(dm),
            "reporting_agent": ReportingAgent(dm),
            "goal_agent": GoalAgent(dm, notification_agent),
            "notification_agent": notification_agent
        }
    return _agents

@router.get("/overview")
async def get_overview(user_role: str, user_id: Optional[str] = None):
    """Get dashboard overview data"""
    agents = get_agents()
    data_manager = get_data_manager()
    
    if user_role == "employee":
        # Employee dashboard
        employees = data_manager.load_data("employees") or []
        current_employee = next((e for e in employees if str(e.get("id")) == str(user_id)), None)
        if not current_employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        # Get employee performance
        eval_data = agents["performance_agent"].evaluate_employee(current_employee.get("id"), save=False)
        
        # Get tasks
        tasks = data_manager.load_data("tasks") or []
        my_tasks = [t for t in tasks if t.get("assigned_to") == current_employee.get("id")]
        
        # Get goals
        all_goals = agents["goal_agent"].get_all_goals()
        my_goals = [g for g in all_goals if str(g.get("employee_id", "")) == str(current_employee.get("id")) or str(g.get("user_id", "")) == str(current_employee.get("id"))]
        
        return {
            "role": "employee",
            "performance": eval_data or {},
            "tasks": {
                "total": len(my_tasks),
                "completed": len([t for t in my_tasks if t.get("status") == "completed"]),
                "in_progress": len([t for t in my_tasks if t.get("status") == "in_progress"]),
                "pending": len([t for t in my_tasks if t.get("status") == "pending"]),
                "active": len([t for t in my_tasks if t.get("status") in ["pending", "in_progress"]])
            },
            "goals": {
                "total": len(my_goals),
                "completed": len([g for g in my_goals if g.get("status") == "completed"])
            }
        }
    else:
        # Manager/Owner dashboard
        overview = agents["reporting_agent"].generate_overview_report()
        employees = data_manager.load_data("employees") or []
        tasks = data_manager.load_data("tasks") or []
        
        # Calculate team KPIs
        team_performance_scores = []
        team_completion_rates = []
        team_on_time_rates = []
        
        for emp in employees:
            emp_id = emp.get("id")
            eval_data = agents["performance_agent"].evaluate_employee(emp_id, save=False)
            if eval_data:
                team_performance_scores.append(eval_data.get('performance_score', 0))
                team_completion_rates.append(eval_data.get('completion_rate', 0))
                team_on_time_rates.append(eval_data.get('on_time_rate', 0))
        
        avg_team_performance = sum(team_performance_scores) / len(team_performance_scores) if team_performance_scores else 0
        avg_completion_rate = sum(team_completion_rates) / len(team_completion_rates) if team_completion_rates else 0
        avg_on_time_rate = sum(team_on_time_rates) / len(team_on_time_rates) if team_on_time_rates else 0
        
        # Employee rankings
        employee_rankings = []
        for emp in employees:
            emp_id = emp.get("id")
            eval_data = agents["performance_agent"].evaluate_employee(emp_id, save=False)
            if eval_data:
                employee_rankings.append({
                    "name": emp.get("name", "Unknown"),
                    "employee_id": emp_id,
                    "performance_score": eval_data.get('performance_score', 0),
                    "completion_rate": eval_data.get('completion_rate', 0),
                    "on_time_rate": eval_data.get('on_time_rate', 0),
                    "rank": eval_data.get('rank', 'N/A')
                })
        
        employee_rankings.sort(key=lambda x: x['performance_score'], reverse=True)
        for idx, emp in enumerate(employee_rankings):
            emp['rank'] = idx + 1
        
        return {
            "role": "manager",
            "overview": overview,
            "team_kpis": {
                "avg_performance": avg_team_performance,
                "avg_completion_rate": avg_completion_rate,
                "avg_on_time_rate": avg_on_time_rate,
                "team_size": len(employees)
            },
            "employee_rankings": employee_rankings[:10]  # Top 10
        }

