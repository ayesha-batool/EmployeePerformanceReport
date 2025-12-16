"""
ML Performance Scoring Model
Uses Random Forest / XGBoost to predict performance scores
Inputs: Task quality, Feedback sentiment, Attendance trend, Workload balance
Output: Performance score (0-100)
"""
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, List
import pickle
import os
from datetime import datetime, timedelta
import json

try:
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import mean_squared_error, r2_score
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


class PerformanceScorer:
    """ML-based performance scoring model"""
    
    def __init__(self, model_type: str = "random_forest", model_path: Optional[str] = None):
        """
        Initialize performance scorer
        
        Args:
            model_type: "random_forest" or "xgboost"
            model_path: Path to saved model (optional)
        """
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler() if SKLEARN_AVAILABLE else None
        self.is_trained = False
        self.model_path = model_path or "models/performance_scorer.pkl"
        
        # Load existing model if available
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        elif os.path.exists(self.model_path):
            self.load_model(self.model_path)
    
    def extract_features(self, employee_data: Dict[str, Any]) -> np.ndarray:
        """
        Extract features from employee data
        
        Features:
        1. Task quality (average task completion quality score)
        2. Feedback sentiment (average sentiment from feedback)
        3. Attendance trend (recent attendance rate trend)
        4. Workload balance (workload distribution score)
        """
        features = []
        
        # 1. Task Quality (0-1 normalized)
        tasks = employee_data.get("tasks", [])
        if tasks:
            completed_tasks = [t for t in tasks if t.get("status") == "completed"]
            if completed_tasks:
                # Calculate quality based on on-time completion, priority handling
                quality_scores = []
                for task in completed_tasks:
                    quality = 0.5  # Base quality
                    # On-time completion bonus
                    if task.get("due_date"):
                        try:
                            due = datetime.fromisoformat(task["due_date"])
                            completed = datetime.fromisoformat(task.get("completed_at", task.get("updated_at", "")))
                            if completed <= due:
                                quality += 0.3
                        except:
                            pass
                    # Priority handling
                    if task.get("priority") == "high" and task.get("status") == "completed":
                        quality += 0.2
                    quality_scores.append(min(1.0, quality))
                task_quality = np.mean(quality_scores) if quality_scores else 0.5
            else:
                task_quality = 0.5
        else:
            task_quality = 0.5
        
        features.append(task_quality)
        
        # 2. Feedback Sentiment (0-1 normalized, 0.5 = neutral)
        feedbacks = employee_data.get("feedbacks", [])
        if feedbacks:
            # Simple sentiment: positive feedback = higher score
            positive_count = sum(1 for f in feedbacks if f.get("type") == "positive" or f.get("rating", 0) > 3)
            negative_count = sum(1 for f in feedbacks if f.get("type") == "negative" or f.get("rating", 0) < 3)
            total = len(feedbacks)
            if total > 0:
                sentiment = 0.5 + (positive_count - negative_count) / (total * 2)
                sentiment = max(0.0, min(1.0, sentiment))
            else:
                sentiment = 0.5
        else:
            sentiment = 0.5
        
        features.append(sentiment)
        
        # 3. Attendance Trend (0-1 normalized)
        attendance_records = employee_data.get("attendance", [])
        if attendance_records and len(attendance_records) >= 7:
            # Calculate recent attendance rate (last 30 days)
            recent_records = attendance_records[-30:] if len(attendance_records) > 30 else attendance_records
            present_count = sum(1 for a in recent_records if a.get("status") == "present")
            attendance_rate = present_count / len(recent_records) if recent_records else 0.95
        else:
            attendance_rate = 0.95  # Default to good attendance
        
        features.append(attendance_rate)
        
        # 4. Workload Balance (0-1 normalized, 0.5 = balanced)
        tasks = employee_data.get("tasks", [])
        if tasks:
            # Calculate workload balance: optimal is 0.5 (not too few, not too many)
            total_tasks = len(tasks)
            active_tasks = len([t for t in tasks if t.get("status") in ["pending", "in_progress"]])
            
            # Normalize: 5-10 active tasks = optimal (0.5)
            if active_tasks == 0:
                workload_balance = 0.3  # Underloaded
            elif active_tasks <= 5:
                workload_balance = 0.4 + (active_tasks / 5) * 0.1
            elif active_tasks <= 10:
                workload_balance = 0.5  # Optimal
            elif active_tasks <= 15:
                workload_balance = 0.5 - ((active_tasks - 10) / 5) * 0.2
            else:
                workload_balance = 0.2  # Overloaded
        else:
            workload_balance = 0.3  # No tasks = underloaded
        
        features.append(workload_balance)
        
        return np.array(features).reshape(1, -1)
    
    def train(self, training_data: List[Dict[str, Any]], target_scores: List[float]):
        """
        Train the model on historical data
        
        Args:
            training_data: List of employee data dictionaries
            target_scores: List of actual performance scores (0-100)
        """
        if not SKLEARN_AVAILABLE:
            print("❌ scikit-learn not available. Cannot train model.")
            return
        
        # Extract features
        X = np.array([self.extract_features(emp_data).flatten() for emp_data in training_data])
        y = np.array(target_scores)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )
        
        # Train model
        if self.model_type == "random_forest":
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
        elif self.model_type == "xgboost" and XGBOOST_AVAILABLE:
            self.model = xgb.XGBRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            )
        else:
            print("⚠️ XGBoost not available, using Random Forest")
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"✅ Model trained. MSE: {mse:.2f}, R²: {r2:.2f}")
        self.is_trained = True
        
        # Save model
        self.save_model()
    
    def predict(self, employee_data: Dict[str, Any]) -> float:
        """
        Predict performance score for an employee
        
        Args:
            employee_data: Employee data dictionary with tasks, feedbacks, attendance, etc.
        
        Returns:
            Predicted performance score (0-100)
        """
        if not self.is_trained or self.model is None:
            # Fallback to simple calculation if model not trained
            return self._fallback_score(employee_data)
        
        # Extract features
        features = self.extract_features(employee_data)
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Predict
        score = self.model.predict(features_scaled)[0]
        
        # Ensure score is in valid range
        return max(0.0, min(100.0, float(score)))
    
    def _fallback_score(self, employee_data: Dict[str, Any]) -> float:
        """Fallback scoring if model not trained"""
        features = self.extract_features(employee_data).flatten()
        # Simple weighted average
        weights = [0.3, 0.25, 0.25, 0.2]  # task_quality, sentiment, attendance, workload
        score = sum(f * w for f, w in zip(features, weights)) * 100
        return max(0.0, min(100.0, score))
    
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

