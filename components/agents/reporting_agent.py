"""
Reporting Agent - AI-powered project reports and analytics
"""
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import json
from components.managers.data_manager import DataManager
from components.managers.ai_client import AIClient
from components.managers.event_bus import get_event_bus


class ReportingAgent:
    """Comprehensive reporting and analytics agent"""
    
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        self.ai_client = AIClient()
        self.event_bus = get_event_bus()
        
        if not self.ai_client.enabled:
            print("⚠️ WARNING: AI is not enabled. Reporting requires AI. Set USE_AI=true and configure API key.")
    
    def generate_project_report(self, project_id: str) -> Dict[str, Any]:
        """Generate detailed project report"""
        projects = self.data_manager.load_data("projects") or []
        tasks = self.data_manager.load_data("tasks") or []
        employees = self.data_manager.load_data("employees") or []
        
        project = next((p for p in projects if p.get("id") == project_id), None)
        if not project:
            return {"error": "Project not found"}
        
        project_tasks = [t for t in tasks if t.get("project_id") == project_id]
        
        # Calculate metrics
        total_tasks = len(project_tasks)
        completed_tasks = len([t for t in project_tasks if t.get("status") == "completed"])
        pending_tasks = len([t for t in project_tasks if t.get("status") == "pending"])
        in_progress_tasks = len([t for t in project_tasks if t.get("status") == "in_progress"])
        
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Use AI to calculate project health
        previous_health = project.get("health_score")
        health_score = self._ai_calculate_project_health(project, project_tasks)
        
        # Publish project health changed event if changed (event-driven)
        if previous_health and abs(previous_health - health_score) > 5:
            self.event_bus.publish_event(
                EventType.PROJECT_HEALTH_CHANGED,
                {
                    "project": project,
                    "health_score": health_score,
                    "previous_score": previous_health
                },
                source="ReportingAgent"
            )
        
        # Use AI to identify risks
        risks = self._ai_identify_project_risks(project, project_tasks)
        
        # Publish risk events for detected risks (event-driven)
        for risk in risks:
            self.event_bus.publish_event(
                EventType.RISK_DETECTED,
                {"risk": risk, "project_id": project_id},
                source="ReportingAgent"
            )
        
        # Resource allocation
        resource_allocation = self._analyze_resource_allocation(project_tasks, employees)
        
        # Estimate completion date
        estimated_completion = self._estimate_completion_date(project, project_tasks)
        
        report = {
            "project_id": project_id,
            "project_name": project.get("name"),
            "status": project.get("status"),
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "in_progress_tasks": in_progress_tasks,
            "completion_rate": round(completion_rate, 2),
            "health_score": health_score,
            "risks": risks,
            "resource_allocation": resource_allocation,
            "estimated_completion_date": estimated_completion,
            "generated_at": datetime.now().isoformat()
        }
        
        return report
    
    def generate_overview_report(self) -> Dict[str, Any]:
        """Generate system overview report"""
        projects = self.data_manager.load_data("projects") or []
        tasks = self.data_manager.load_data("tasks") or []
        employees = self.data_manager.load_data("employees") or []
        performance_data = self.data_manager.load_data("performances") or []
        
        # Project statistics
        total_projects = len(projects)
        active_projects = len([p for p in projects if p.get("status") == "active"])
        completed_projects = len([p for p in projects if p.get("status") == "completed"])
        
        # Task statistics
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t.get("status") == "completed"])
        overdue_tasks = self._count_overdue_tasks(tasks)
        
        # Employee statistics
        total_employees = len(employees)
        active_employees = total_employees  # All employees are active
        
        # Performance statistics
        avg_performance = self._calculate_avg_performance(performance_data)
        
        # Resource allocation
        resource_utilization = self._calculate_resource_utilization(tasks, employees)
        
        overview = {
            "projects": {
                "total": total_projects,
                "active": active_projects,
                "completed": completed_projects
            },
            "tasks": {
                "total": total_tasks,
                "completed": completed_tasks,
                "overdue": overdue_tasks,
                "completion_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            },
            "employees": {
                "total": total_employees,
                "active": active_employees
            },
            "performance": {
                "average_score": round(avg_performance, 2)
            },
            "resource_utilization": resource_utilization,
            "generated_at": datetime.now().isoformat()
        }
        
        return overview
    
    def _ai_calculate_project_health(self, project: Dict[str, Any], tasks: List[Dict[str, Any]]) -> float:
        """Use AI to calculate project health score - no rule-based formulas"""
        if not self.ai_client.enabled:
            # Simple fallback
            if not tasks:
                return 100.0
            completion_rate = len([t for t in tasks if t.get("status") == "completed"]) / len(tasks) * 100
            return completion_rate
        
        try:
            project_data = {
                "project_name": project.get("name", ""),
                "status": project.get("status", ""),
                "deadline": project.get("deadline", ""),
                "total_tasks": len(tasks),
                "completed_tasks": len([t for t in tasks if t.get("status") == "completed"]),
                "overdue_tasks": self._count_overdue_tasks(tasks),
                "task_details": tasks[:20]  # Sample of tasks
            }
            
            system_prompt = """You are a project health analyst. Analyze project data and calculate a health score (0-100).
Consider: completion rate, deadline proximity, task status, team performance, risks.

Return ONLY a number between 0 and 100 representing the project health score."""
            
            user_prompt = f"""Calculate health score for this project:
{json.dumps(project_data, indent=2, default=str)}

Current date: {datetime.now().isoformat()}

Return only the score number (0-100)."""
            
            response = self.ai_client.chat(
                [{"role": "user", "content": user_prompt}],
                system_prompt=system_prompt,
                temperature=0.3,
                max_tokens=50
            )
            
            if response:
                import re
                numbers = re.findall(r'\d+\.?\d*', response)
                if numbers:
                    score = float(numbers[0])
                    return min(max(score, 0), 100)
            
            # Fallback
            if not tasks:
                return 100.0
            completion_rate = len([t for t in tasks if t.get("status") == "completed"]) / len(tasks) * 100
            return completion_rate
        except Exception as e:
            print(f"AI project health calculation error: {e}")
            if not tasks:
                return 100.0
            completion_rate = len([t for t in tasks if t.get("status") == "completed"]) / len(tasks) * 100
            return completion_rate
    
    
    def _ai_identify_project_risks(self, project: Dict[str, Any], tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Use AI to identify project risks - no rule-based thresholds"""
        if not self.ai_client.enabled:
            return []
        
        try:
            project_data = {
                "project_name": project.get("name", ""),
                "status": project.get("status", ""),
                "deadline": project.get("deadline", ""),
                "total_tasks": len(tasks),
                "completed_tasks": len([t for t in tasks if t.get("status") == "completed"]),
                "overdue_tasks": self._count_overdue_tasks(tasks),
                "tasks": tasks[:20]  # Sample
            }
            
            system_prompt = """You are a project risk analyst. Identify risks in project data.
Return JSON array with risks, each having: type, severity (low/medium/high/critical), description, and relevant details.
Return empty array [] if no risks found."""
            
            user_prompt = f"""Identify risks for this project:
{json.dumps(project_data, indent=2, default=str)}

Current date: {datetime.now().isoformat()}

Return JSON array of risks."""
            
            response = self.ai_client.chat(
                [{"role": "user", "content": user_prompt}],
                system_prompt=system_prompt,
                temperature=0.3,
                max_tokens=500
            )
            
            if response:
                try:
                    # Try to parse JSON from response
                    if "```json" in response:
                        response = response.split("```json")[1].split("```")[0].strip()
                    elif "```" in response:
                        response = response.split("```")[1].split("```")[0].strip()
                    
                    risks = json.loads(response)
                    if isinstance(risks, list):
                        return risks
                except:
                    # If JSON parsing fails, try to extract risk info
                    pass
            
            return []
        except Exception as e:
            print(f"AI risk identification error: {e}")
            return []
    
    
    def _analyze_resource_allocation(self, tasks: List[Dict[str, Any]], employees: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze resource allocation"""
        allocation = {}
        for employee in employees:
            emp_id = employee.get("id")
            emp_tasks = [t for t in tasks if t.get("assigned_to") == emp_id]
            allocation[emp_id] = {
                "name": employee.get("name"),
                "task_count": len(emp_tasks),
                "completed": len([t for t in emp_tasks if t.get("status") == "completed"]),
                "pending": len([t for t in emp_tasks if t.get("status") == "pending"])
            }
        return allocation
    
    def _estimate_completion_date(self, project: Dict[str, Any], tasks: List[Dict[str, Any]]) -> Optional[str]:
        """Estimate project completion date"""
        incomplete_tasks = [t for t in tasks if t.get("status") != "completed"]
        if not incomplete_tasks:
            return datetime.now().isoformat()
        
        # Get average completion time
        completed_tasks = [t for t in tasks if t.get("status") == "completed"]
        if completed_tasks:
            completion_times = []
            for task in completed_tasks:
                if task.get("created_at") and task.get("completed_at"):
                    try:
                        created = datetime.fromisoformat(task["created_at"])
                        completed = datetime.fromisoformat(task["completed_at"])
                        completion_times.append((completed - created).days)
                    except:
                        pass
            
            if completion_times:
                avg_days = sum(completion_times) / len(completion_times)
                estimated = datetime.now() + timedelta(days=int(avg_days * len(incomplete_tasks)))
                return estimated.isoformat()
        
        return None
    
    def _count_overdue_tasks(self, tasks: List[Dict[str, Any]]) -> int:
        """Count overdue tasks"""
        return len(self._get_overdue_tasks(tasks))
    
    def _get_overdue_tasks(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get overdue tasks"""
        overdue = []
        for task in tasks:
            if task.get("status") != "completed" and task.get("due_date"):
                try:
                    due_date = datetime.fromisoformat(task["due_date"])
                    if due_date < datetime.now():
                        overdue.append(task)
                except:
                    pass
        return overdue
    
    def _calculate_avg_performance(self, performance_data: List[Dict[str, Any]]) -> float:
        """Calculate average performance score"""
        if not performance_data:
            return 0.0
        
        # Get latest evaluation for each employee
        latest_scores = {}
        for perf in performance_data:
            emp_id = perf.get("employee_id")
            score = perf.get("performance_score", 0)
            if emp_id not in latest_scores or perf.get("evaluated_at", "") > latest_scores[emp_id].get("evaluated_at", ""):
                latest_scores[emp_id] = perf
        
        scores = [p.get("performance_score", 0) for p in latest_scores.values()]
        return sum(scores) / len(scores) if scores else 0.0
    
    def _calculate_resource_utilization(self, tasks: List[Dict[str, Any]], employees: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate resource utilization"""
        total_employees = len(employees)
        employees_with_tasks = len(set([t.get("assigned_to") for t in tasks if t.get("assigned_to")]))
        
        utilization_rate = (employees_with_tasks / total_employees * 100) if total_employees > 0 else 0
        
        return {
            "total_employees": total_employees,
            "employees_with_tasks": employees_with_tasks,
            "utilization_rate": round(utilization_rate, 2)
        }

