"""
Promotion Classification Model
Uses ML classification (Random Forest / XGBoost) to predict promotion probability
Inputs: Performance, Consistency, Skills, Leadership
Output: Promotion probability (0-1)
"""
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, List
import pickle
import os
from datetime import datetime, timedelta

try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("⚠️ scikit-learn not available. Install with: pip install scikit-learn")

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("⚠️ xgboost not available. Install with: pip install xgboost")


class PromotionClassifier:
    """ML-based promotion probability classifier"""
    
    def __init__(self, model_type: str = "random_forest", model_path: Optional[str] = None):
        """
        Initialize promotion classifier
        
        Args:
            model_type: "random_forest" or "xgboost"
            model_path: Path to saved model (optional)
        """
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler() if SKLEARN_AVAILABLE else None
        self.is_trained = False
        self.model_path = model_path or "models/promotion_classifier.pkl"
        
        # Load existing model if available
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        elif os.path.exists(self.model_path):
            self.load_model(self.model_path)
    
    def extract_features(self, employee_data: Dict[str, Any]) -> np.ndarray:
        """
        Extract features from employee data
        
        Features:
        1. Performance (average performance score)
        2. Consistency (performance variance/consistency)
        3. Skills (skill level and diversity)
        4. Leadership (leadership indicators)
        """
        features = []
        
        # 1. Performance (0-1 normalized from 0-100)
        performance_history = employee_data.get("performance_history", [])
        if performance_history:
            performance_scores = [p.get("performance_score", 50) for p in performance_history]
            avg_performance = np.mean(performance_scores)
            performance_normalized = avg_performance / 100.0  # Normalize to 0-1
        else:
            performance_normalized = 0.5  # Default: average
        
        features.append(performance_normalized)
        
        # 2. Consistency (0-1, higher = more consistent)
        if performance_history and len(performance_history) >= 3:
            performance_scores = [p.get("performance_score", 50) for p in performance_history]
            # Calculate coefficient of variation (lower = more consistent)
            mean_score = np.mean(performance_scores)
            std_score = np.std(performance_scores)
            if mean_score > 0:
                cv = std_score / mean_score
                # Invert: lower CV = higher consistency score
                consistency = max(0.0, min(1.0, 1.0 - (cv * 2)))  # Scale CV to 0-1
            else:
                consistency = 0.5
        else:
            consistency = 0.5  # Default: moderate consistency
        
        features.append(consistency)
        
        # 3. Skills (0-1 normalized)
        skills = employee_data.get("skills", {})
        if isinstance(skills, str):
            try:
                import json
                skills = json.loads(skills)
            except:
                skills = {}
        
        if skills and isinstance(skills, dict):
            # Calculate average skill level (assuming 1-5 scale)
            skill_levels = [v for v in skills.values() if isinstance(v, (int, float))]
            if skill_levels:
                avg_skill_level = np.mean(skill_levels)
                # Normalize from 1-5 scale to 0-1
                skills_normalized = (avg_skill_level - 1) / 4.0
                
                # Bonus for skill diversity (number of skills)
                num_skills = len(skill_levels)
                diversity_bonus = min(0.2, num_skills / 20.0)  # Max 0.2 bonus
                skills_normalized = min(1.0, skills_normalized + diversity_bonus)
            else:
                skills_normalized = 0.3  # Low skills
        else:
            skills_normalized = 0.3  # Default: low skills
        
        features.append(skills_normalized)
        
        # 4. Leadership (0-1 normalized)
        leadership_score = 0.0
        
        # Leadership indicators:
        # - Mentoring others (if tracking available)
        # - Team leadership roles
        # - High responsibility tasks
        # - Positive feedback on leadership
        
        tasks = employee_data.get("tasks", [])
        if tasks:
            # High priority tasks indicate responsibility
            high_priority_tasks = len([t for t in tasks if t.get("priority") == "high"])
            if len(tasks) > 0:
                leadership_score += (high_priority_tasks / len(tasks)) * 0.3
        
        # Goals achievement indicates reliability
        goals = employee_data.get("goals", [])
        if goals:
            completed_goals = len([g for g in goals if g.get("status") == "completed"])
            if len(goals) > 0:
                leadership_score += (completed_goals / len(goals)) * 0.3
        
        # Positive feedback on leadership
        feedbacks = employee_data.get("feedbacks", [])
        if feedbacks:
            leadership_feedback = [f for f in feedbacks 
                                  if "leadership" in f.get("title", "").lower() 
                                  or "leadership" in f.get("description", "").lower()]
            if leadership_feedback:
                positive_leadership = sum(1 for f in leadership_feedback 
                                        if f.get("type") == "positive" or f.get("rating", 3) >= 4)
                if len(leadership_feedback) > 0:
                    leadership_score += (positive_leadership / len(leadership_feedback)) * 0.4
        
        # Role-based leadership indicator
        employee = employee_data.get("employee", {})
        role = employee.get("role", "").lower()
        if role in ["manager", "team_lead", "supervisor", "director"]:
            leadership_score += 0.2
        
        leadership_normalized = min(1.0, leadership_score)
        features.append(leadership_normalized)
        
        return np.array(features).reshape(1, -1)
    
    def train(self, training_data: List[Dict[str, Any]], promotion_labels: List[int]):
        """
        Train the model on historical data
        
        Args:
            training_data: List of employee data dictionaries
            promotion_labels: List of labels (1 = promoted, 0 = not promoted)
        """
        if not SKLEARN_AVAILABLE:
            print("❌ scikit-learn not available. Cannot train model.")
            return
        
        # Extract features
        X = np.array([self.extract_features(emp_data).flatten() for emp_data in training_data])
        y = np.array(promotion_labels)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train model
        if self.model_type == "random_forest":
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1,
                class_weight="balanced"  # Handle imbalanced data
            )
        elif self.model_type == "xgboost" and XGBOOST_AVAILABLE:
            self.model = xgb.XGBClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42,
                eval_metric="logloss"
            )
        else:
            print("⚠️ XGBoost not available, using Random Forest")
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1,
                class_weight="balanced"
            )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        
        try:
            auc = roc_auc_score(y_test, y_pred_proba)
        except:
            auc = 0.0
        
        print(f"✅ Model trained. Accuracy: {accuracy:.2f}, Precision: {precision:.2f}, "
              f"Recall: {recall:.2f}, F1: {f1:.2f}, AUC: {auc:.2f}")
        self.is_trained = True
        
        # Save model
        self.save_model()
    
    def predict_probability(self, employee_data: Dict[str, Any]) -> float:
        """
        Predict promotion probability for an employee
        
        Args:
            employee_data: Employee data dictionary with performance, skills, etc.
        
        Returns:
            Promotion probability (0-1)
        """
        if not self.is_trained or self.model is None:
            # Fallback to simple calculation if model not trained
            return self._fallback_probability(employee_data)
        
        # Extract features
        features = self.extract_features(employee_data)
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Predict probability
        probability = self.model.predict_proba(features_scaled)[0, 1]
        
        # Ensure probability is in valid range
        return max(0.0, min(1.0, float(probability)))
    
    def predict(self, employee_data: Dict[str, Any], threshold: float = 0.5) -> Dict[str, Any]:
        """
        Predict promotion readiness with detailed output
        
        Args:
            employee_data: Employee data dictionary
            threshold: Probability threshold for promotion recommendation
        
        Returns:
            {
                "probability": float (0-1),
                "recommended": bool,
                "confidence": str,
                "factors": Dict[str, float],
                "recommendations": List[str]
            }
        """
        probability = self.predict_probability(employee_data)
        
        # Extract individual feature contributions
        features = self.extract_features(employee_data).flatten()
        factors = {
            "performance": features[0],
            "consistency": features[1],
            "skills": features[2],
            "leadership": features[3]
        }
        
        # Determine confidence
        if probability >= 0.8:
            confidence = "high"
        elif probability >= 0.6:
            confidence = "medium"
        elif probability >= 0.4:
            confidence = "low"
        else:
            confidence = "very_low"
        
        # Generate recommendations
        recommendations = self._generate_recommendations(factors, probability)
        
        return {
            "probability": probability,
            "recommended": probability >= threshold,
            "confidence": confidence,
            "factors": factors,
            "recommendations": recommendations
        }
    
    def _fallback_probability(self, employee_data: Dict[str, Any]) -> float:
        """Fallback probability calculation if model not trained"""
        features = self.extract_features(employee_data).flatten()
        
        # Simple weighted average
        weights = [0.35, 0.25, 0.20, 0.20]  # performance, consistency, skills, leadership
        probability = sum(f * w for f, w in zip(features, weights))
        
        return max(0.0, min(1.0, probability))
    
    def _generate_recommendations(self, factors: Dict[str, float], probability: float) -> List[str]:
        """Generate recommendations based on factors"""
        recommendations = []
        
        if factors["performance"] < 0.7:
            recommendations.append("Focus on improving performance scores")
        
        if factors["consistency"] < 0.6:
            recommendations.append("Work on maintaining consistent performance")
        
        if factors["skills"] < 0.6:
            recommendations.append("Develop additional skills and expertise")
        
        if factors["leadership"] < 0.5:
            recommendations.append("Take on leadership opportunities and responsibilities")
        
        if probability < 0.5:
            recommendations.append("Continue development in multiple areas before promotion consideration")
        elif probability >= 0.7:
            recommendations.append("Strong candidate for promotion - consider promotion opportunities")
        
        return recommendations if recommendations else ["Continue current development path"]
    
    def save_model(self, path: Optional[str] = None):
        """Save trained model"""
        if not self.is_trained or self.model is None:
            return
        
        path = path or self.model_path
        os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
        
        model_data = {
            "model": self.model,
            "scaler": self.scaler,
            "model_type": self.model_type,
            "is_trained": self.is_trained
        }
        
        with open(path, "wb") as f:
            pickle.dump(model_data, f)
        
        print(f"✅ Model saved to {path}")
    
    def load_model(self, path: str):
        """Load trained model"""
        try:
            with open(path, "rb") as f:
                model_data = pickle.load(f)
            
            self.model = model_data["model"]
            self.scaler = model_data["scaler"]
            self.model_type = model_data.get("model_type", "random_forest")
            self.is_trained = model_data.get("is_trained", True)
            
            print(f"✅ Model loaded from {path}")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.is_trained = False

