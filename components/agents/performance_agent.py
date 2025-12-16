"""
Performance Agent - ML/AI-powered performance evaluation
Streamlined version - no legacy code
"""
from datetime import datetime
from typing import Dict, Any, Optional, List
import json
import re
from components.managers.data_manager import DataManager
from components.managers.ai_client import AIClient
from components.managers.event_bus import get_event_bus, EventType
from components.ml.performance_scorer import PerformanceScorer


class EnhancedPerformanceAgent:
    """ML/AI-powered performance evaluation"""
    
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        self.ai_client = AIClient()
        self.event_bus = get_event_bus()
        self.ml_scorer = PerformanceScorer(model_type="random_forest")
    
    def evaluate_employee(self, employee_id: str, save: bool = True) -> Dict[str, Any]:
        """Evaluate employee performance using ML model"""
        tasks = self.data_manager.load_data("tasks") or []
        employees = self.data_manager.load_data("employees") or []
        employee_tasks = [t for t in tasks if t.get("assigned_to") == employee_id]
        
        # Calculate basic metrics
        total_tasks = len(employee_tasks)
        completed_tasks = len([t for t in employee_tasks if t.get("status") == "completed"])
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Calculate on-time completion
        on_time_tasks = sum(1 for t in employee_tasks 
                           if t.get("status") == "completed" and self._is_on_time(t))
        on_time_rate = (on_time_tasks / completed_tasks * 100) if completed_tasks > 0 else 0
        
        # Use ML model for scoring
        employee_data = {
            "tasks": employee_tasks,
            "feedbacks": self._get_feedbacks(employee_id),
            "attendance": [],
            "workload": len([t for t in employee_tasks if t.get("status") in ["pending", "in_progress"]])
        }
        
        performance_score = self.ml_scorer.predict(employee_data)
        if not self.ml_scorer.is_trained:
            performance_score = self._ai_fallback_score(employee_id, employee_tasks, completion_rate, on_time_rate)
        
        # Calculate rank and trend
        rank = self._calculate_rank_simple(employee_id, performance_score)
        trend = self._calculate_trend_simple(employee_id, performance_score)
        
        evaluation = {
            "employee_id": employee_id,
            "performance_score": round(performance_score, 2),
            "completion_rate": round(completion_rate, 2),
            "on_time_rate": round(on_time_rate, 2),
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "rank": rank,
            "trend": trend,
            "evaluated_at": datetime.now().isoformat()
        }
        
        # Publish events
        self.event_bus.publish_event(EventType.PERFORMANCE_EVALUATED, {
            "employee_id": employee_id,
            "performance": evaluation,
            "previous_performance": self._get_previous(employee_id)
        }, source="PerformanceAgent")
        
        previous_trend = self._get_previous_trend(employee_id)
        if previous_trend and previous_trend != trend:
            self.event_bus.publish_event(EventType.PERFORMANCE_TREND_CHANGED, {
                "employee_id": employee_id,
                "trend": trend,
                "previous_trend": previous_trend,
                "performance": evaluation
            }, source="PerformanceAgent")
        
        return evaluation
    
    def _is_on_time(self, task: Dict[str, Any]) -> bool:
        """Check if task completed on time"""
        if not task.get("due_date"):
            return True
        try:
            due = datetime.fromisoformat(task["due_date"])
            completed = datetime.fromisoformat(task.get("completed_at", task.get("updated_at", "")))
            return completed <= due
        except:
            return True
    
    def _get_feedbacks(self, employee_id: str) -> List[Dict[str, Any]]:
        """Get employee feedbacks"""
        feedbacks = self.data_manager.load_data("feedback") or []
        return [f for f in feedbacks if str(f.get("employee_id", "")) == str(employee_id)]
    
    def _ai_fallback_score(self, employee_id: str, tasks: List[Dict[str, Any]], 
                          completion_rate: float, on_time_rate: float) -> float:
        """AI fallback if ML not trained"""
        if not self.ai_client.enabled:
            return 50.0
        try:
            data = {"employee_id": employee_id, "completion_rate": completion_rate, "on_time_rate": on_time_rate}
            response = self.ai_client.chat(
                [{"role": "user", "content": f"Calculate performance score (0-100): {json.dumps(data)}"}],
                system_prompt="Return only a number 0-100", temperature=0.3, max_tokens=50
            )
            if response:
                numbers = re.findall(r'\d+\.?\d*', response)
                if numbers:
                    return min(max(float(numbers[0]), 0), 100)
        except:
            pass
        return 50.0
    
    def _calculate_rank_simple(self, employee_id: str, score: float) -> int:
        """Simple rank calculation"""
        performances = self.data_manager.load_data("performances") or []
        scores = [p.get("performance_score", 0) for p in performances]
        scores.append(score)
        scores.sort(reverse=True)
        return scores.index(score) + 1
    
    def _calculate_trend_simple(self, employee_id: str, current_score: float) -> str:
        """Simple trend calculation"""
        if not self.ai_client.enabled:
            return "stable"
        try:
            performances = self.data_manager.load_data("performances") or []
            emp_perf = [p for p in performances if p.get("employee_id") == employee_id]
            if len(emp_perf) < 2:
                return "stable"
            
            historical = sorted(emp_perf, key=lambda x: x.get("evaluated_at", ""), reverse=True)[:5]
            response = self.ai_client.chat(
                [{"role": "user", "content": f"Trend: current={current_score}, history={[p.get('performance_score', 0) for p in historical]}. Return: improving/declining/stable"}],
                system_prompt="Return one word", temperature=0.2, max_tokens=10
            )
            if response:
                resp = response.lower().strip()
                if "improving" in resp:
                    return "improving"
                elif "declining" in resp:
                    return "declining"
        except:
            pass
        return "stable"
    
    def _get_previous(self, employee_id: str) -> Optional[Dict[str, Any]]:
        """Get previous performance"""
        performances = self.data_manager.load_data("performances") or []
        emp_perf = [p for p in performances if p.get("employee_id") == employee_id]
        return sorted(emp_perf, key=lambda x: x.get("evaluated_at", ""), reverse=True)[0] if emp_perf else None
    
    def _get_previous_trend(self, employee_id: str) -> Optional[str]:
        """Get previous trend"""
        previous = self._get_previous(employee_id)
        return previous.get("trend") if previous else None

