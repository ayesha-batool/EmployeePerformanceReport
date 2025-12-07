"""
OKR Agent - Personal OKR (Objectives and Key Results) tracking
"""
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from components.managers.data_manager import DataManager
from components.agents.notification_agent import NotificationAgent


class OKRAgent:
    """OKR (Objectives and Key Results) management agent"""
    
    def __init__(self, data_manager: DataManager, notification_agent: Optional[NotificationAgent] = None):
        self.data_manager = data_manager
        self.notification_agent = notification_agent
    
    def create_okr(self, employee_id: str, okr_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new OKR"""
        if not okr_data.get("objective"):
            return {"success": False, "error": "Objective is required"}
        
        if not okr_data.get("key_results") or len(okr_data.get("key_results", [])) == 0:
            return {"success": False, "error": "At least one key result is required"}
        
        okrs = self.data_manager.load_data("okrs") or []
        
        okr = {
            "id": f"okr_{len(okrs) + 1}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "employee_id": employee_id,
            "objective": okr_data["objective"],
            "description": okr_data.get("description", ""),
            "quarter": okr_data.get("quarter"),  # Q1, Q2, Q3, Q4, or custom
            "year": okr_data.get("year", datetime.now().year),
            "key_results": okr_data["key_results"],  # List of {title, target, current, unit}
            "team_goal_alignment": okr_data.get("team_goal_alignment", []),  # List of related team goal IDs
            "status": "active",
            "progress_percentage": 0.0,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "review_date": okr_data.get("review_date"),
            "completed_at": None
        }
        
        # Calculate initial progress
        okr["progress_percentage"] = self._calculate_okr_progress(okr)
        
        okrs.append(okr)
        self.data_manager.save_data("okrs", okrs)
        
        return {"success": True, "okr": okr}
    
    def update_key_result(self, okr_id: str, key_result_index: int, current_value: float,
                         notes: Optional[str] = None) -> Dict[str, Any]:
        """Update a key result's current value"""
        okrs = self.data_manager.load_data("okrs") or []
        
        for okr in okrs:
            if okr.get("id") == okr_id:
                if 0 <= key_result_index < len(okr.get("key_results", [])):
                    okr["key_results"][key_result_index]["current"] = current_value
                    if notes:
                        okr["key_results"][key_result_index]["notes"] = notes
                    okr["key_results"][key_result_index]["updated_at"] = datetime.now().isoformat()
                    
                    # Recalculate overall progress
                    okr["progress_percentage"] = self._calculate_okr_progress(okr)
                    okr["updated_at"] = datetime.now().isoformat()
                    
                    # Check if OKR is completed
                    if okr["progress_percentage"] >= 100:
                        okr["status"] = "completed"
                        okr["completed_at"] = datetime.now().isoformat()
                    
                    self.data_manager.save_data("okrs", okrs)
                    
                    return {"success": True, "okr": okr}
                else:
                    return {"success": False, "error": "Invalid key result index"}
        
        return {"success": False, "error": "OKR not found"}
    
    def _calculate_okr_progress(self, okr: Dict[str, Any]) -> float:
        """Calculate overall OKR progress based on key results"""
        key_results = okr.get("key_results", [])
        if not key_results:
            return 0.0
        
        total_progress = 0.0
        for kr in key_results:
            target = kr.get("target", 0)
            current = kr.get("current", 0)
            if target > 0:
                kr_progress = min((current / target) * 100, 100)  # Cap at 100%
                total_progress += kr_progress
        
        return total_progress / len(key_results) if key_results else 0.0
    
    def get_employee_okrs(self, employee_id: str, status: Optional[str] = None,
                         quarter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get OKRs for an employee"""
        okrs = self.data_manager.load_data("okrs") or []
        
        employee_okrs = [o for o in okrs if o.get("employee_id") == employee_id]
        
        if status:
            employee_okrs = [o for o in employee_okrs if o.get("status") == status]
        
        if quarter:
            employee_okrs = [o for o in employee_okrs if o.get("quarter") == quarter]
        
        # Sort by created_at descending
        employee_okrs.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        return employee_okrs
    
    def align_with_team_goals(self, okr_id: str, team_goal_ids: List[str]) -> Dict[str, Any]:
        """Align OKR with team goals"""
        okrs = self.data_manager.load_data("okrs") or []
        
        for okr in okrs:
            if okr.get("id") == okr_id:
                okr["team_goal_alignment"] = team_goal_ids
                okr["updated_at"] = datetime.now().isoformat()
                self.data_manager.save_data("okrs", okrs)
                return {"success": True, "okr": okr}
        
        return {"success": False, "error": "OKR not found"}
    
    def get_okr_statistics(self, employee_id: str) -> Dict[str, Any]:
        """Get OKR statistics for an employee"""
        okrs = self.get_employee_okrs(employee_id)
        
        total = len(okrs)
        active = len([o for o in okrs if o.get("status") == "active"])
        completed = len([o for o in okrs if o.get("status") == "completed"])
        
        # Average progress
        avg_progress = sum(o.get("progress_percentage", 0) for o in okrs) / total if total > 0 else 0
        
        # Group by quarter
        by_quarter = {}
        for okr in okrs:
            quarter = okr.get("quarter", "Unknown")
            if quarter not in by_quarter:
                by_quarter[quarter] = {"total": 0, "completed": 0, "avg_progress": 0}
            by_quarter[quarter]["total"] += 1
            if okr.get("status") == "completed":
                by_quarter[quarter]["completed"] += 1
            by_quarter[quarter]["avg_progress"] += okr.get("progress_percentage", 0)
        
        # Calculate averages
        for quarter_data in by_quarter.values():
            if quarter_data["total"] > 0:
                quarter_data["avg_progress"] = quarter_data["avg_progress"] / quarter_data["total"]
        
        return {
            "total_okrs": total,
            "active_okrs": active,
            "completed_okrs": completed,
            "completion_rate": (completed / total * 100) if total > 0 else 0,
            "average_progress": avg_progress,
            "by_quarter": by_quarter,
            "recent_okrs": okrs[:5]  # Last 5
        }

