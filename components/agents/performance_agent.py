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
            "workload": len([t for t in employee_tasks if t.get("status") in ["pending", "in_progress"]])
        }
        
        # DEBUG: Check ML model status
        print(f"🔍 [DEBUG] ML Model Trained: {self.ml_scorer.is_trained}")
        print(f"🔍 [DEBUG] AI Client Enabled: {self.ai_client.enabled}")
        print(f"🔍 [DEBUG] AI Provider: {self.ai_client.provider if hasattr(self.ai_client, 'provider') else 'N/A'}")
        
        performance_score = self.ml_scorer.predict(employee_data)
        method_used = "ML Model"
        
        if not self.ml_scorer.is_trained:
            print(f"🔍 [DEBUG] ML model not trained, using fallback...")
            performance_score = self._ai_fallback_score(employee_id, employee_tasks, completion_rate, on_time_rate)
            if self.ai_client.enabled:
                method_used = "AI Fallback"
            else:
                method_used = "Simple Fallback (Weighted Formula)"
        
        print(f"🔍 [DEBUG] Performance Score: {performance_score:.2f}% (Method: {method_used})")
        print(f"🔍 [DEBUG] Completion Rate: {completion_rate:.2f}%")
        print(f"🔍 [DEBUG] On-Time Rate: {on_time_rate:.2f}%")
        
        # Calculate rank and trend
        rank = self._calculate_rank_simple(employee_id, performance_score)
        trend = self._calculate_trend_simple(employee_id, performance_score)
        
        # Generate AI feedback based on performance
        ai_feedback = self._generate_ai_feedback(
            employee_id, performance_score, completion_rate, on_time_rate,
            total_tasks, completed_tasks, employee_tasks, trend
        )
        
        evaluation = {
            "employee_id": employee_id,
            "performance_score": round(performance_score, 2),
            "completion_rate": round(completion_rate, 2),
            "on_time_rate": round(on_time_rate, 2),
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "rank": rank,
            "trend": trend,
            "ai_feedback": ai_feedback,
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
            print(f"🔍 [DEBUG] AI not enabled, returning default score 50.0%")
            return 50.0
        
        print(f"🔍 [DEBUG] Using AI Fallback (Provider: {self.ai_client.provider if hasattr(self.ai_client, 'provider') else 'N/A'})")
        print(f"🔍 [DEBUG] AI Input: completion_rate={completion_rate:.2f}%, on_time_rate={on_time_rate:.2f}%")
        
        try:
            data = {"employee_id": employee_id, "completion_rate": completion_rate, "on_time_rate": on_time_rate}
            response = self.ai_client.chat(
                [{"role": "user", "content": f"Calculate performance score (0-100): {json.dumps(data)}"}],
                system_prompt="Return only a number 0-100", temperature=0.3, max_tokens=50
            )
            print(f"🔍 [DEBUG] AI Response: {response}")
            if response:
                numbers = re.findall(r'\d+\.?\d*', response)
                if numbers:
                    score = min(max(float(numbers[0]), 0), 100)
                    print(f"🔍 [DEBUG] AI Calculated Score: {score:.2f}%")
                    return score
        except Exception as e:
            print(f"🔍 [DEBUG] AI Error: {e}")
            pass
        print(f"🔍 [DEBUG] AI fallback failed, returning default score 50.0%")
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
    
    def _generate_ai_feedback(self, employee_id: str, performance_score: float,
                             completion_rate: float, on_time_rate: float,
                             total_tasks: int, completed_tasks: int,
                             employee_tasks: List[Dict[str, Any]], trend: str) -> str:
        """Generate AI-powered feedback based on performance metrics"""
        if not self.ai_client.enabled:
            # Fallback feedback if AI not enabled
            if performance_score >= 80:
                return "Excellent performance! Keep up the great work. Continue maintaining high standards and consider taking on more challenging tasks."
            elif performance_score >= 60:
                return "Good performance overall. Focus on completing more tasks and maintaining consistency to improve your score further."
            else:
                return "There's room for improvement. Focus on completing tasks on time and increasing your task completion rate."
        
        try:
            # Get employee name
            employees = self.data_manager.load_data("employees") or []
            employee = next((e for e in employees if str(e.get("id")) == str(employee_id)), None)
            employee_name = employee.get("name", "Employee") if employee else "Employee"
            
            # Get feedback summary
            feedbacks = self._get_feedbacks(employee_id)
            feedback_count = len(feedbacks)
            avg_rating = sum([f.get("rating", 0) for f in feedbacks if f.get("rating")]) / len([f for f in feedbacks if f.get("rating")]) if [f for f in feedbacks if f.get("rating")] else 0
            
            # Get goals summary
            goals = self.data_manager.load_data("goals") or []
            employee_goals = [g for g in goals if str(g.get("employee_id", "")) == str(employee_id) or str(g.get("user_id", "")) == str(employee_id)]
            active_goals = len([g for g in employee_goals if g.get("status") in ["active", "in_progress"]])
            achieved_goals = len([g for g in employee_goals if g.get("status") == "achieved"])
            
            # Prepare performance summary
            performance_summary = {
                "employee_name": employee_name,
                "performance_score": round(performance_score, 2),
                "completion_rate": round(completion_rate, 2),
                "on_time_rate": round(on_time_rate, 2),
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "trend": trend,
                "feedback_received": feedback_count,
                "average_feedback_rating": round(avg_rating, 1) if avg_rating > 0 else None,
                "active_goals": active_goals,
                "achieved_goals": achieved_goals
            }
            
            # Create AI prompt
            system_prompt = """You are a performance management expert. Provide constructive, actionable feedback based on employee performance metrics. 
            Be specific, encouraging, and focus on areas for improvement while acknowledging strengths. 
            Keep feedback professional and concise (2-3 paragraphs)."""
            
            user_prompt = f"""Analyze this employee's performance and provide personalized feedback:

Performance Summary:
{json.dumps(performance_summary, indent=2)}

Provide feedback that:
1. Acknowledges strengths
2. Identifies specific areas for improvement
3. Offers actionable recommendations
4. Is encouraging and professional

Format your response as 2-3 paragraphs without bullet points."""
            
            print(f"🔍 [DEBUG] Generating AI feedback for {employee_name}...")
            response = self.ai_client.chat(
                [{"role": "user", "content": user_prompt}],
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=300
            )
            
            if response:
                print(f"🔍 [DEBUG] AI Feedback generated successfully")
                return response.strip()
            else:
                return self._get_fallback_feedback(performance_score)
                
        except Exception as e:
            print(f"🔍 [DEBUG] Error generating AI feedback: {e}")
            return self._get_fallback_feedback(performance_score)
    
    def _get_fallback_feedback(self, performance_score: float) -> str:
        """Fallback feedback if AI generation fails"""
        if performance_score >= 80:
            return "Excellent performance! You're consistently completing tasks on time and maintaining high quality standards. Keep up the outstanding work and consider taking on additional responsibilities to further develop your skills."
        elif performance_score >= 60:
            return "Good performance overall. You're making steady progress. To improve further, focus on increasing your task completion rate and maintaining consistency in meeting deadlines. Consider seeking feedback from colleagues to identify areas for growth."
        else:
            return "There's significant room for improvement. Focus on completing more tasks, meeting deadlines consistently, and maintaining quality standards. Consider breaking down larger tasks into smaller, manageable steps and prioritize your workload effectively."

