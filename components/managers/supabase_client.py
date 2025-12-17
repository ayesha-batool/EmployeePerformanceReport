"""
Supabase Client for Database Operations
Replaces local JSON files and API calls with direct Supabase access
"""
import os
import time
from typing import Dict, Any, Optional, List, Callable
from supabase import create_client, Client
from datetime import datetime
import json

# Try to load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, use system environment variables

# Import httpx for timeout configuration
try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False


class SupabaseClient:
    """Client for Supabase database operations with retry logic and error handling"""
    
    def __init__(self, max_retries: int = 3, retry_delay: float = 1.0, timeout: float = 30.0):
        """
        Initialize Supabase client with retry logic
        
        Args:
            max_retries: Maximum number of retry attempts (default: 3)
            retry_delay: Initial delay between retries in seconds (default: 1.0)
            timeout: Request timeout in seconds (default: 30.0)
        """
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.timeout = timeout
        
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_ANON_KEY must be set in environment variables.\n"
                "Create a .env file with:\n"
                "SUPABASE_URL=https://your-project.supabase.co\n"
                "SUPABASE_ANON_KEY=your-anon-key"
            )
        
        # Create Supabase client
        # Note: Supabase Python client uses httpx internally, but doesn't expose timeout config directly
        # We'll handle retries and timeouts in our wrapper methods instead
        try:
            self.client: Client = create_client(supabase_url, supabase_key)
        except Exception as e:
            raise ValueError(f"Failed to create Supabase client: {str(e)}")
    
    def _retry_operation(self, operation: Callable, *args, **kwargs) -> Any:
        """
        Retry an operation with exponential backoff
        
        Args:
            operation: Function to retry
            *args: Positional arguments for operation
            **kwargs: Keyword arguments for operation
            
        Returns:
            Result of the operation
            
        Raises:
            Exception: If all retries fail
        """
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                return operation(*args, **kwargs)
            except Exception as e:
                last_exception = e
                error_str = str(e).lower()
                
                # Check if it's a retryable error
                retryable_errors = [
                    "10035",  # Windows non-blocking socket error
                    "readerror",
                    "timeout",
                    "connection",
                    "network",
                    "socket",
                    "temporarily unavailable"
                ]
                
                is_retryable = any(err in error_str for err in retryable_errors)
                
                if not is_retryable or attempt == self.max_retries - 1:
                    # Not retryable or last attempt
                    raise
                
                # Exponential backoff
                delay = self.retry_delay * (2 ** attempt)
                print(f"⚠️  Supabase operation failed (attempt {attempt + 1}/{self.max_retries}): {str(e)[:100]}")
                print(f"   Retrying in {delay:.1f} seconds...")
                time.sleep(delay)
        
        # If we get here, all retries failed
        raise last_exception
    
    # Employees
    def get_employees(self) -> List[Dict[str, Any]]:
        """Get all employees"""
        def _get():
            response = self.client.table("employees").select("*").execute()
            return [self._format_item(item) for item in response.data]
        return self._retry_operation(_get)
    
    def get_employee(self, employee_id: str) -> Optional[Dict[str, Any]]:
        """Get employee by ID"""
        def _get():
            response = self.client.table("employees").select("*").eq("id", employee_id).execute()
            return self._format_item(response.data[0]) if response.data else None
        return self._retry_operation(_get)
    
    def get_employee_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get employee by email"""
        def _get():
            response = self.client.table("employees").select("*").eq("email", email).execute()
            return self._format_item(response.data[0]) if response.data else None
        return self._retry_operation(_get)
    
    def create_employee(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create employee"""
        # Handle skills as JSONB
        employee_data = data.copy()
        if "skills" in employee_data and isinstance(employee_data["skills"], dict):
            employee_data["skills"] = json.dumps(employee_data["skills"])
        response = self.client.table("employees").insert(employee_data).execute()
        return self._format_item(response.data[0])
    
    def update_employee(self, employee_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update employee"""
        employee_data = data.copy()
        if "skills" in employee_data and isinstance(employee_data["skills"], dict):
            employee_data["skills"] = json.dumps(employee_data["skills"])
        response = self.client.table("employees").update(employee_data).eq("id", employee_id).execute()
        return self._format_item(response.data[0]) if response.data else {}
    
    def delete_employee(self, employee_id: str) -> bool:
        """Delete employee"""
        self.client.table("employees").delete().eq("id", employee_id).execute()
        return True
    
    # Tasks
    def get_tasks(self, employee_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all tasks, optionally filtered by employee"""
        def _get():
            query = self.client.table("tasks").select("*")
            if employee_id:
                query = query.eq("assigned_to", employee_id)
            response = query.execute()
            return [self._format_item(item) for item in response.data]
        return self._retry_operation(_get)
    
    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task by ID"""
        def _get():
            response = self.client.table("tasks").select("*").eq("id", task_id).execute()
            return self._format_item(response.data[0]) if response.data else None
        return self._retry_operation(_get)
    
    def create_task(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create task"""
        # Convert string IDs to UUIDs if needed
        task_data = self._prepare_data(data, ["assigned_to", "project_id"])
        response = self.client.table("tasks").insert(task_data).execute()
        return self._format_item(response.data[0])
    
    def update_task(self, task_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update task"""
        try:
            task_data = self._prepare_data(data, ["assigned_to", "project_id"])
            response = self.client.table("tasks").update(task_data).eq("id", task_id).execute()
            if not response.data:
                raise ValueError(f"No data returned from Supabase update operation for task {task_id}")
            return self._format_item(response.data[0])
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error updating task in Supabase: {error_msg}")
            print(f"📋 Task ID: {task_id}")
            print(f"📋 Update data: {task_data}")
            import traceback
            traceback.print_exc()
            raise Exception(f"Failed to update task in database: {error_msg}")
    
    def delete_task(self, task_id: str) -> bool:
        """Delete task"""
        self.client.table("tasks").delete().eq("id", task_id).execute()
        return True
    
    # Projects
    def get_projects(self) -> List[Dict[str, Any]]:
        """Get all projects"""
        def _get():
            response = self.client.table("projects").select("*").execute()
            return [self._format_item(item) for item in response.data]
        return self._retry_operation(_get)
    
    def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Get project by ID"""
        def _get():
            response = self.client.table("projects").select("*").eq("id", project_id).execute()
            return self._format_item(response.data[0]) if response.data else None
        return self._retry_operation(_get)
    
    def create_project(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create project"""
        response = self.client.table("projects").insert(data).execute()
        return self._format_item(response.data[0])
    
    def update_project(self, project_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update project"""
        response = self.client.table("projects").update(data).eq("id", project_id).execute()
        return self._format_item(response.data[0]) if response.data else {}
    
    def delete_project(self, project_id: str) -> bool:
        """Delete project"""
        self.client.table("projects").delete().eq("id", project_id).execute()
        return True
    
    # Performances
    def get_performances(self, employee_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get performances, optionally filtered by employee"""
        def _get():
            query = self.client.table("performances").select("*").order("evaluation_date", desc=True)
            if employee_id:
                query = query.eq("employee_id", employee_id)
            response = query.execute()
            return [self._format_item(item) for item in response.data]
        return self._retry_operation(_get)
    
    def create_performance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create performance evaluation"""
        response = self.client.table("performances").insert(data).execute()
        return self._format_item(response.data[0])
    
    # Goals
    def get_goals(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get goals, optionally filtered by user"""
        def _get():
            query = self.client.table("performance_goals").select("*")
            if user_id:
                query = query.eq("user_id", user_id)
            response = query.execute()
            return [self._format_item(item) for item in response.data]
        return self._retry_operation(_get)
    
    def create_goal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create goal"""
        # Convert user_id to UUID format if needed
        goal_data = self._prepare_data(data, ["user_id"])
        response = self.client.table("performance_goals").insert(goal_data).execute()
        return self._format_item(response.data[0])
    
    def update_goal(self, goal_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update goal"""
        # Filter out invalid fields and map deadline to target_date if needed
        valid_fields = ["title", "description", "goal_type", "target_value", "current_value", 
                       "start_date", "target_date", "status", "updated_at"]
        filtered_data = {}
        for key, value in data.items():
            if key in valid_fields:
                filtered_data[key] = value
            elif key == "deadline" and "target_date" not in filtered_data:
                # Map deadline to target_date if deadline is provided but target_date is not
                filtered_data["target_date"] = value
        
        # Remove None values to avoid clearing fields unintentionally
        filtered_data = {k: v for k, v in filtered_data.items() if v is not None}
        
        response = self.client.table("performance_goals").update(filtered_data).eq("id", goal_id).execute()
        return self._format_item(response.data[0]) if response.data else {}
    
    # Feedback
    def get_feedback(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get feedback, optionally filtered by user"""
        def _get():
            query = self.client.table("peer_feedback").select("*")
            if user_id:
                query = query.eq("employee_id", user_id)
            response = query.execute()
            return [self._format_item(item) for item in response.data]
        return self._retry_operation(_get)
    
    def create_feedback(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create feedback"""
        # Convert IDs to UUID format
        feedback_data = self._prepare_data(data, ["employee_id", "reviewer_id", "project_id"])
        response = self.client.table("peer_feedback").insert(feedback_data).execute()
        return self._format_item(response.data[0])
    
    # Notifications
    def get_notifications(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get notifications, optionally filtered by user"""
        def _get():
            query = self.client.table("notifications").select("*").order("created_at", desc=True)
            if user_id:
                query = query.eq("user_id", user_id)
            response = query.execute()
            return [self._format_item(item) for item in response.data]
        return self._retry_operation(_get)
    
    def create_notification(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create notification"""
        response = self.client.table("notifications").insert(data).execute()
        return self._format_item(response.data[0])
    
    def mark_notification_read(self, notification_id: str) -> Dict[str, Any]:
        """Mark notification as read"""
        response = self.client.table("notifications").update({"is_read": True}).eq("id", notification_id).execute()
        return self._format_item(response.data[0]) if response.data else {}
    
    # Reviews
    def get_reviews(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get reviews, optionally filtered by user"""
        query = self.client.table("performance_reviews").select("*")
        if user_id:
            query = query.eq("employee_id", user_id)
        response = query.execute()
        return [self._format_item(item) for item in response.data]
    
    def create_review(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create review"""
        response = self.client.table("performance_reviews").insert(data).execute()
        return self._format_item(response.data[0])
    
    # Skills
    def get_skills(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get skills, optionally filtered by user"""
        query = self.client.table("skill_assessments").select("*")
        if user_id:
            query = query.eq("user_id", user_id)
        response = query.execute()
        return [self._format_item(item) for item in response.data]
    
    def assess_skill(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create skill assessment"""
        response = self.client.table("skill_assessments").insert(data).execute()
        return self._format_item(response.data[0])
    
    # Achievements
    def get_achievements(self, employee_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get achievements, optionally filtered by employee"""
        try:
            query = self.client.table("achievements").select("*").order("created_at", desc=True)
            if employee_id:
                query = query.eq("employee_id", employee_id)
            response = query.execute()
            return [self._format_item(item) for item in response.data]
        except Exception as e:
            error_msg = str(e)
            # Check if table doesn't exist
            if "Could not find the table" in error_msg or "PGRST205" in error_msg:
                print(f"⚠️ Achievements table not found in Supabase. Please run the schema SQL to create it.")
                print(f"   The table definition is in supabase_schema.sql (lines 143-161)")
            raise
    
    def create_achievement(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create achievement"""
        # Prepare achievement data - clean UUIDs and handle dates
        achievement_data = {}
        for key, value in data.items():
            if value is None:
                # Include None values for optional fields like description, but skip for required fields
                if key in ["description", "related_task_id", "related_project_id", "verified_by", "verified_at", "verification_notes"]:
                    continue
                # For date fields, we might want to allow None, but let's skip them if None
                if key in ["start_date", "end_date"]:
                    continue
            
            # Clean UUID fields (remove spaces, newlines)
            if key in ["employee_id", "related_task_id", "related_project_id"]:
                achievement_data[key] = str(value).strip().replace(" ", "").replace("\n", "").replace("\r", "")
            # Handle date fields - ensure they're in proper format
            elif key in ["start_date", "end_date"]:
                if isinstance(value, str):
                    # If it's already a string, use it directly (should be ISO format)
                    achievement_data[key] = value
                else:
                    achievement_data[key] = value
            else:
                achievement_data[key] = value
        
        # Insert into database
        try:
            # Validate employee_id is a valid UUID format
            import re
            uuid_pattern = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)
            employee_id = achievement_data.get("employee_id")
            if employee_id and not uuid_pattern.match(str(employee_id)):
                raise ValueError(f"Invalid employee_id format: '{employee_id}'. Expected UUID format (e.g., '123e4567-e89b-12d3-a456-426614174000'). Please ensure the employee exists in the database with a valid UUID.")
            
            response = self.client.table("achievements").insert(achievement_data).execute()
            if not response.data:
                raise ValueError("No data returned from Supabase insert operation")
            return self._format_item(response.data[0])
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error creating achievement in Supabase: {error_msg}")
            print(f"📋 Achievement data being inserted: {achievement_data}")
            import traceback
            traceback.print_exc()
            # Re-raise with more context
            raise Exception(f"Failed to create achievement in database: {error_msg}")
    
    def update_achievement(self, achievement_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update achievement"""
        try:
            # Handle date fields - ensure they're in proper format
            update_data = {}
            for key, value in data.items():
                if value is None:
                    update_data[key] = None
                elif key in ["start_date", "end_date"]:
                    if isinstance(value, str):
                        # If it's already a string, use it directly (should be ISO format)
                        update_data[key] = value
                    elif isinstance(value, datetime):
                        # If it's a datetime object, convert to ISO format
                        update_data[key] = value.isoformat()
                    else:
                        update_data[key] = value
                else:
                    update_data[key] = value
            
            response = self.client.table("achievements").update(update_data).eq("id", achievement_id).execute()
            if not response.data:
                raise ValueError(f"No data returned from Supabase update operation for achievement {achievement_id}")
            return self._format_item(response.data[0])
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error updating achievement in Supabase: {error_msg}")
            print(f"📋 Achievement ID: {achievement_id}")
            print(f"📋 Update data: {update_data}")
            import traceback
            traceback.print_exc()
            raise Exception(f"Failed to update achievement in database: {error_msg}")
    
    def delete_achievement(self, achievement_id: str) -> bool:
        """Delete achievement"""
        self.client.table("achievements").delete().eq("id", achievement_id).execute()
        return True
    
    def _prepare_data(self, data: Dict[str, Any], uuid_fields: List[str]) -> Dict[str, Any]:
        """Prepare data for Supabase insertion (handle UUIDs)"""
        prepared = {}
        for key, value in data.items():
            if key in uuid_fields and value:
                # Keep UUID as string (Supabase handles it)
                prepared[key] = value
            elif value is not None:
                prepared[key] = value
        return prepared
    
    def _format_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Format database item to match expected format"""
        from datetime import datetime
        formatted = {}
        for key, value in item.items():
            # Convert UUID to string (keep as is)
            if isinstance(value, str):
                formatted[key] = value
            # Convert datetime to ISO string
            elif isinstance(value, datetime):
                formatted[key] = value.isoformat()
            # Keep JSONB as dict
            elif isinstance(value, dict):
                formatted[key] = value
            # Convert Decimal to float
            elif hasattr(value, '__float__'):
                formatted[key] = float(value)
            else:
                formatted[key] = value
        
        # Map target_date to deadline for backward compatibility with UI code
        if "target_date" in formatted and "deadline" not in formatted:
            formatted["deadline"] = formatted["target_date"]
        
        return formatted

