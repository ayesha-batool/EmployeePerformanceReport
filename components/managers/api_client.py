"""
API Client for Frontend - Connects Streamlit to FastAPI backend
"""
import httpx
import os
from typing import Dict, Any, Optional, List

class APIClient:
    """Client for communicating with FastAPI backend"""
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or os.getenv("API_BASE_URL", "http://localhost:8003")
        self.client = httpx.Client(timeout=30.0)
    
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Login user"""
        response = self.client.post(
            f"{self.base_url}/api/frontend/auth/login",
            json={"email": email, "password": password}
        )
        response.raise_for_status()
        return response.json()
    
    def get_dashboard_overview(self, user_role: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Get dashboard overview"""
        params = {"user_role": user_role}
        if user_id:
            params["user_id"] = user_id
        response = self.client.get(f"{self.base_url}/api/dashboard/overview", params=params)
        response.raise_for_status()
        return response.json()
    
    def get_goals(self, user_id: Optional[str] = None, user_role: str = "employee") -> List[Dict[str, Any]]:
        """Get goals"""
        params = {"user_role": user_role}
        if user_id:
            params["user_id"] = user_id
        response = self.client.get(f"{self.base_url}/api/frontend/goals", params=params)
        response.raise_for_status()
        return response.json().get("goals", [])
    
    def create_goal(self, goal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create goal"""
        response = self.client.post(f"{self.base_url}/api/frontend/goals", json=goal_data)
        response.raise_for_status()
        return response.json()
    
    def get_feedback(self, employee_id: Optional[str] = None, user_role: str = "employee") -> List[Dict[str, Any]]:
        """Get feedback"""
        params = {"user_role": user_role}
        if employee_id:
            params["employee_id"] = employee_id
        response = self.client.get(f"{self.base_url}/api/frontend/feedback", params=params)
        response.raise_for_status()
        return response.json().get("feedbacks", [])
    
    def create_feedback(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create feedback"""
        response = self.client.post(f"{self.base_url}/api/frontend/feedback", json=feedback_data)
        response.raise_for_status()
        return response.json()
    
    def respond_to_feedback(self, feedback_id: str, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Respond to feedback"""
        response = self.client.post(
            f"{self.base_url}/api/frontend/feedback/{feedback_id}/respond",
            json=response_data
        )
        response.raise_for_status()
        return response.json()
    
    def get_overview_report(self) -> Dict[str, Any]:
        """Get overview report"""
        response = self.client.get(f"{self.base_url}/api/frontend/reports/overview")
        response.raise_for_status()
        return response.json()
    
    def get_project_report(self, project_id: str) -> Dict[str, Any]:
        """Get project report"""
        response = self.client.get(f"{self.base_url}/api/frontend/reports/project/{project_id}")
        response.raise_for_status()
        return response.json()
    
    def export_data(self, data_type: str) -> Dict[str, Any]:
        """Export data"""
        response = self.client.post(
            f"{self.base_url}/api/frontend/reports/export",
            params={"data_type": data_type}
        )
        response.raise_for_status()
        return response.json()
    
    def get_employees(self) -> List[Dict[str, Any]]:
        """Get employees"""
        response = self.client.get(f"{self.base_url}/api/frontend/employees")
        response.raise_for_status()
        return response.json().get("employees", [])
    
    def get_projects(self, user_id: Optional[str] = None, user_role: str = "employee") -> List[Dict[str, Any]]:
        """Get projects"""
        params = {"user_role": user_role}
        if user_id:
            params["user_id"] = user_id
        response = self.client.get(f"{self.base_url}/api/frontend/projects", params=params)
        response.raise_for_status()
        return response.json().get("projects", [])
    
    def update_task(self, task_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update task"""
        response = self.client.post(
            f"{self.base_url}/api/frontend/tasks/{task_id}/update",
            json=updates
        )
        response.raise_for_status()
        return response.json()

