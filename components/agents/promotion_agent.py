"""
Promotion Agent - ML-powered promotion eligibility and probability prediction
Uses classification model to predict promotion probability
Inputs: Performance, Consistency, Skills, Leadership
Output: Promotion probability (0-1)
"""
from typing import Dict, Any, Optional, List
from datetime import datetime
from components.managers.data_manager import DataManager
from components.ml.promotion_classifier import PromotionClassifier


class PromotionAgent:
    """ML-powered promotion eligibility analysis agent"""
    
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        # Initialize ML promotion classifier
        self.classifier = PromotionClassifier(model_type="random_forest")
    
    def analyze_promotion_eligibility(self, employee_id: str) -> Dict[str, Any]:
        """
        Analyze promotion eligibility for an employee
        
        Args:
            employee_id: Employee ID
        
        Returns:
            {
                "employee_id": str,
                "probability": float (0-1),
                "recommended": bool,
                "confidence": str,
                "factors": {
                    "performance": float,
                    "consistency": float,
                    "skills": float,
                    "leadership": float
                },
                "recommendations": List[str],
                "analysis_date": str
            }
        """
        # Get employee data
        employees = self.data_manager.load_data("employees") or []
        employee = next((e for e in employees if str(e.get("id", "")) == str(employee_id)), None)
        
        if not employee:
            return {
                "employee_id": employee_id,
                "probability": 0.0,
                "recommended": False,
                "confidence": "very_low",
                "factors": {},
                "recommendations": ["Employee not found"],
                "error": "Employee not found",
                "analysis_date": datetime.now().isoformat()
            }
        
        # Get related data
        tasks = self.data_manager.load_data("tasks") or []
        employee_tasks = [t for t in tasks if str(t.get("assigned_to", "")) == str(employee_id)]
        
        goals = self.data_manager.load_data("goals") or []
        employee_goals = [g for g in goals 
                         if str(g.get("employee_id", "")) == str(employee_id) 
                         or str(g.get("user_id", "")) == str(employee_id)]
        
        feedbacks = self.data_manager.load_data("feedback") or []
        employee_feedbacks = [f for f in feedbacks 
                            if str(f.get("employee_id", "")) == str(employee_id)]
        
        performances = self.data_manager.load_data("performances") or []
        employee_performances = [
            p for p in performances 
            if str(p.get("employee_id", "")) == str(employee_id)
        ]
        
        # Get skills
        skills = employee.get("skills", {})
        if isinstance(skills, str):
            try:
                import json
                skills = json.loads(skills)
            except:
                skills = {}
        
        # Prepare employee data for ML model
        employee_data = {
            "employee": employee,
            "tasks": employee_tasks,
            "goals": employee_goals,
            "feedbacks": employee_feedbacks,
            "performance_history": employee_performances[-12:] if employee_performances else [],  # Last 12 evaluations
            "skills": skills
        }
        
        # Use ML classifier to predict promotion probability
        prediction = self.classifier.predict(employee_data, threshold=0.6)
        
        return {
            "employee_id": employee_id,
            "employee_name": employee.get("name", ""),
            "current_role": employee.get("role", ""),
            "probability": prediction["probability"],
            "recommended": prediction["recommended"],
            "confidence": prediction["confidence"],
            "factors": prediction["factors"],
            "recommendations": prediction["recommendations"],
            "analysis_date": datetime.now().isoformat()
        }
    
    def get_promotion_recommendations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get promotion recommendations for all employees
        
        Args:
            limit: Maximum number of recommendations to return
        
        Returns:
            List of promotion analyses sorted by probability
        """
        employees = self.data_manager.load_data("employees") or []
        
        recommendations = []
        for employee in employees:
            employee_id = employee.get("id")
            if employee_id:
                analysis = self.analyze_promotion_eligibility(employee_id)
                if analysis.get("probability", 0) > 0.4:  # Only include candidates with >40% probability
                    recommendations.append(analysis)
        
        # Sort by probability (descending)
        recommendations.sort(key=lambda x: x.get("probability", 0), reverse=True)
        
        return recommendations[:limit]
    
    def compare_promotion_candidates(self, employee_ids: List[str]) -> Dict[str, Any]:
        """
        Compare multiple employees for promotion
        
        Args:
            employee_ids: List of employee IDs to compare
        
        Returns:
            Comparison analysis with rankings and recommendations
        """
        analyses = []
        for employee_id in employee_ids:
            analysis = self.analyze_promotion_eligibility(employee_id)
            analyses.append(analysis)
        
        # Sort by probability
        analyses.sort(key=lambda x: x.get("probability", 0), reverse=True)
        
        # Find top candidate
        top_candidate = analyses[0] if analyses else None
        
        # Calculate average factors
        if analyses:
            avg_factors = {
                "performance": sum(a.get("factors", {}).get("performance", 0) for a in analyses) / len(analyses),
                "consistency": sum(a.get("factors", {}).get("consistency", 0) for a in analyses) / len(analyses),
                "skills": sum(a.get("factors", {}).get("skills", 0) for a in analyses) / len(analyses),
                "leadership": sum(a.get("factors", {}).get("leadership", 0) for a in analyses) / len(analyses)
            }
        else:
            avg_factors = {}
        
        return {
            "candidates": analyses,
            "top_candidate": top_candidate,
            "average_factors": avg_factors,
            "comparison_date": datetime.now().isoformat()
        }
    
    def train_model(self, training_data: Optional[List[Dict[str, Any]]] = None, 
                   promotion_labels: Optional[List[int]] = None) -> Dict[str, Any]:
        """
        Train the promotion classifier model
        
        Args:
            training_data: Optional list of employee data (if None, uses all employees)
            promotion_labels: Optional list of labels (1 = promoted, 0 = not promoted)
        
        Returns:
            Training results
        """
        if training_data is None or promotion_labels is None:
            # Auto-generate training data from historical data
            # This is a placeholder - in production, you'd use actual promotion history
            employees = self.data_manager.load_data("employees") or []
            training_data = []
            promotion_labels = []
            
            for employee in employees:
                employee_id = employee.get("id")
                if not employee_id:
                    continue
                
                # Get employee data
                tasks = [t for t in self.data_manager.load_data("tasks") or []
                        if str(t.get("assigned_to", "")) == str(employee_id)]
                goals = [g for g in self.data_manager.load_data("goals") or []
                        if str(g.get("employee_id", "")) == str(employee_id) 
                        or str(g.get("user_id", "")) == str(employee_id)]
                feedbacks = [f for f in self.data_manager.load_data("feedback") or []
                            if str(f.get("employee_id", "")) == str(employee_id)]
                performances = [p for p in self.data_manager.load_data("performances") or []
                              if str(p.get("employee_id", "")) == str(employee_id)]
                
                skills = employee.get("skills", {})
                if isinstance(skills, str):
                    try:
                        import json
                        skills = json.loads(skills)
                    except:
                        skills = {}
                
                employee_data = {
                    "employee": employee,
                    "tasks": tasks,
                    "goals": goals,
                    "feedbacks": feedbacks,
                    "performance_history": performances[-12:] if performances else [],
                    "skills": skills
                }
                
                training_data.append(employee_data)
                
                # Label: 1 if role is manager/owner (assumed promoted), 0 otherwise
                role = employee.get("role", "").lower()
                label = 1 if role in ["manager", "owner", "director", "supervisor"] else 0
                promotion_labels.append(label)
        
        # Train model
        self.classifier.train(training_data, promotion_labels)
        
        return {
            "success": True,
            "training_samples": len(training_data),
            "model_type": self.classifier.model_type,
            "message": "Model trained successfully"
        }
