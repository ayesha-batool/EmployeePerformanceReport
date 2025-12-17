"""
Data Manager - Direct Supabase Interface
Simple wrapper around SupabaseClient
"""
from typing import Dict, Any, Optional, List
from components.managers.supabase_client import SupabaseClient


class DataManager:
    """Simple data manager using Supabase directly"""
    
    def __init__(self):
        self.supabase = SupabaseClient()
    
    def load_data(self, filename: str) -> Optional[List[Dict[str, Any]]]:
        """Load data from Supabase"""
        mapping = {
            "employees": "get_employees",
            "tasks": "get_tasks",
            "projects": "get_projects",
            "performances": "get_performances",
            "goals": "get_goals",
            "feedback": "get_feedback",
            "notifications": "get_notifications",
            "achievements": "get_achievements"
        }
        
        method_name = mapping.get(filename)
        if method_name:
            method = getattr(self.supabase, method_name)
            data = method()
            return data if data else []
        return []
    
    def save_data(self, filename: str, data: Any) -> bool:
        """Save data to Supabase (bulk save for backward compatibility)"""
        if not isinstance(data, list):
            return False
        
        try:
            # For bulk saves, update each item
            for item in data:
                item_id = item.get("id")
                if not item_id:
                    continue
                
                # Try update first, then insert if not found
                try:
                    update_data = {k: v for k, v in item.items() if k != "id"}
                    if filename == "tasks":
                        self.supabase.update_task(item_id, update_data)
                    elif filename == "goals":
                        self.supabase.update_goal(item_id, update_data)
                    elif filename == "achievements":
                        self.supabase.update_achievement(item_id, update_data)
                    elif filename == "feedback":
                        self.supabase.update_feedback(item_id, update_data)
                except:
                    # If update fails, try insert
                    try:
                        if filename == "tasks":
                            self.supabase.create_task(item)
                        elif filename == "goals":
                            self.supabase.create_goal(item)
                        elif filename == "achievements":
                            self.supabase.create_achievement(item)
                        elif filename == "feedback":
                            self.supabase.create_feedback(item)
                    except:
                        pass
            return True
        except Exception as e:
            print(f"Error saving {filename}: {e}")
            return False
    
    # Direct access to Supabase methods
    def create_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create task"""
        return self.supabase.create_task(task_data)
    
    def update_task(self, task_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update task"""
        return self.supabase.update_task(task_id, task_data)
    
    def create_goal(self, goal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create goal"""
        return self.supabase.create_goal(goal_data)
    
    def update_goal(self, goal_id: str, goal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update goal"""
        return self.supabase.update_goal(goal_id, goal_data)
    
    def create_feedback(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create feedback"""
        return self.supabase.create_feedback(feedback_data)
    
    def create_achievement(self, achievement_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create achievement"""
        return self.supabase.create_achievement(achievement_data)
    
    def update_achievement(self, achievement_id: str, achievement_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update achievement"""
        return self.supabase.update_achievement(achievement_id, achievement_data)
    
    def create_employee(self, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create employee"""
        return self.supabase.create_employee(employee_data)
    
    def update_employee(self, employee_id: str, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update employee"""
        return self.supabase.update_employee(employee_id, employee_data)
    
    def delete_employee(self, employee_id: str) -> bool:
        """Delete employee"""
        return self.supabase.delete_employee(employee_id)