"""
Predictive Analytics Agent
Uses time-series forecasting (LSTM / Prophet) to predict:
- Future performance
- Burnout risk
- Promotion readiness
"""
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import os

try:
    from tensorflow import keras
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    LSTM_AVAILABLE = True
except ImportError:
    LSTM_AVAILABLE = False
    print("⚠️ TensorFlow not available. Install with: pip install tensorflow")

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False
    print("⚠️ Prophet not available. Install with: pip install prophet")


class PredictiveAnalytics:
    """Time-series forecasting for employee analytics"""
    
    def __init__(self, model_type: str = "prophet"):
        """
        Initialize predictive analytics
        
        Args:
            model_type: "lstm" or "prophet"
        """
        self.model_type = model_type
        self.performance_models = {}  # employee_id -> model
        self.burnout_models = {}
        self.promotion_models = {}
    
    def prepare_performance_data(self, employee_id: str, performance_history: List[Dict[str, Any]]) -> pd.DataFrame:
        """Prepare performance data for time-series analysis"""
        df = pd.DataFrame(performance_history)
        
        if "evaluated_at" in df.columns:
            df["ds"] = pd.to_datetime(df["evaluated_at"])
        else:
            df["ds"] = pd.date_range(end=datetime.now(), periods=len(df), freq="D")
        
        df["y"] = df.get("performance_score", 0)
        df = df.sort_values("ds")
        
        return df[["ds", "y"]]
    
    def predict_future_performance(self, employee_id: str, performance_history: List[Dict[str, Any]], 
                                   days_ahead: int = 30) -> Dict[str, Any]:
        """
        Predict future performance using time-series forecasting
        
        Args:
            employee_id: Employee ID
            performance_history: List of historical performance records
            days_ahead: Number of days to predict ahead
        
        Returns:
            {
                "predicted_score": float,
                "confidence_interval": (lower, upper),
                "trend": "improving" | "declining" | "stable",
                "predictions": List of (date, score) tuples
            }
        """
        if len(performance_history) < 7:
            # Not enough data
            return {
                "predicted_score": performance_history[-1].get("performance_score", 50) if performance_history else 50,
                "confidence_interval": (45, 55),
                "trend": "stable",
                "predictions": []
            }
        
        df = self.prepare_performance_data(employee_id, performance_history)
        
        if self.model_type == "prophet" and PROPHET_AVAILABLE:
            return self._predict_with_prophet(df, days_ahead)
        elif self.model_type == "lstm" and LSTM_AVAILABLE:
            return self._predict_with_lstm(df, days_ahead)
        else:
            # Fallback to simple trend
            return self._predict_simple_trend(df, days_ahead)
    
    def _predict_with_prophet(self, df: pd.DataFrame, days_ahead: int) -> Dict[str, Any]:
        """Predict using Prophet"""
        model = Prophet(yearly_seasonality=False, weekly_seasonality=True, daily_seasonality=False)
        model.fit(df)
        
        # Create future dataframe
        future = model.make_future_dataframe(periods=days_ahead)
        forecast = model.predict(future)
        
        # Get predictions
        predictions = [
            (row["ds"].isoformat(), row["yhat"])
            for _, row in forecast.tail(days_ahead).iterrows()
        ]
        
        # Calculate trend
        recent_scores = df["y"].tail(7).values
        if len(recent_scores) >= 2:
            trend_slope = (recent_scores[-1] - recent_scores[0]) / len(recent_scores)
            if trend_slope > 2:
                trend = "improving"
            elif trend_slope < -2:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "stable"
        
        last_prediction = forecast.tail(1)
        
        return {
            "predicted_score": float(last_prediction["yhat"].iloc[0]),
            "confidence_interval": (
                float(last_prediction["yhat_lower"].iloc[0]),
                float(last_prediction["yhat_upper"].iloc[0])
            ),
            "trend": trend,
            "predictions": predictions
        }
    
    def _predict_with_lstm(self, df: pd.DataFrame, days_ahead: int) -> Dict[str, Any]:
        """Predict using LSTM"""
        # Prepare data
        data = df["y"].values
        lookback = 7  # Use last 7 days to predict next
        
        if len(data) < lookback + days_ahead:
            return self._predict_simple_trend(df, days_ahead)
        
        # Normalize
        mean = np.mean(data)
        std = np.std(data)
        normalized_data = (data - mean) / std
        
        # Create sequences
        X, y = [], []
        for i in range(lookback, len(normalized_data)):
            X.append(normalized_data[i-lookback:i])
            y.append(normalized_data[i])
        
        X, y = np.array(X), np.array(y)
        X = X.reshape((X.shape[0], X.shape[1], 1))
        
        # Build model
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(lookback, 1)),
            Dropout(0.2),
            LSTM(50, return_sequences=False),
            Dropout(0.2),
            Dense(1)
        ])
        model.compile(optimizer="adam", loss="mse")
        
        # Train
        model.fit(X, y, epochs=20, batch_size=32, verbose=0)
        
        # Predict
        last_sequence = normalized_data[-lookback:].reshape(1, lookback, 1)
        predictions = []
        
        for _ in range(days_ahead):
            pred = model.predict(last_sequence, verbose=0)[0, 0]
            predictions.append(pred)
            # Update sequence
            last_sequence = np.append(last_sequence[:, 1:, :], pred.reshape(1, 1, 1), axis=1)
        
        # Denormalize
        predictions = [p * std + mean for p in predictions]
        
        # Calculate trend
        recent_scores = data[-7:]
        if len(recent_scores) >= 2:
            trend_slope = (recent_scores[-1] - recent_scores[0]) / len(recent_scores)
            if trend_slope > 2:
                trend = "improving"
            elif trend_slope < -2:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "stable"
        
        future_dates = pd.date_range(start=df["ds"].iloc[-1] + timedelta(days=1), periods=days_ahead, freq="D")
        predictions_list = [
            (date.isoformat(), float(score))
            for date, score in zip(future_dates, predictions)
        ]
        
        return {
            "predicted_score": float(predictions[-1]),
            "confidence_interval": (
                float(predictions[-1] - std),
                float(predictions[-1] + std)
            ),
            "trend": trend,
            "predictions": predictions_list
        }
    
    def _predict_simple_trend(self, df: pd.DataFrame, days_ahead: int) -> Dict[str, Any]:
        """Simple trend-based prediction"""
        scores = df["y"].values
        if len(scores) < 2:
            return {
                "predicted_score": float(scores[0]) if len(scores) > 0 else 50.0,
                "confidence_interval": (45.0, 55.0),
                "trend": "stable",
                "predictions": []
            }
        
        # Linear trend
        x = np.arange(len(scores))
        slope = np.polyfit(x, scores, 1)[0]
        
        predicted_score = scores[-1] + slope * days_ahead
        
        # Determine trend
        if slope > 0.1:
            trend = "improving"
        elif slope < -0.1:
            trend = "declining"
        else:
            trend = "stable"
        
        return {
            "predicted_score": float(max(0, min(100, predicted_score))),
            "confidence_interval": (
                float(predicted_score - 5),
                float(predicted_score + 5)
            ),
            "trend": trend,
            "predictions": []
        }
    
    def predict_burnout_risk(self, employee_id: str, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict burnout risk
        
        Factors:
        - High workload
        - Long working hours
        - Low performance trend
        - High stress indicators
        - Low engagement
        """
        risk_factors = []
        risk_score = 0.0
        
        # Workload factor
        tasks = employee_data.get("tasks", [])
        active_tasks = len([t for t in tasks if t.get("status") in ["pending", "in_progress"]])
        if active_tasks > 15:
            risk_factors.append("High workload")
            risk_score += 0.3
        elif active_tasks > 10:
            risk_score += 0.15
        
        # Performance trend
        performance_history = employee_data.get("performance_history", [])
        if len(performance_history) >= 3:
            recent_scores = [p.get("performance_score", 50) for p in performance_history[-3:]]
            if recent_scores[-1] < recent_scores[0] - 5:
                risk_factors.append("Declining performance")
                risk_score += 0.25
        
        # Overdue tasks
        overdue_tasks = len([t for t in tasks if t.get("status") != "completed" and t.get("due_date")])
        if overdue_tasks > 3:
            risk_factors.append("Multiple overdue tasks")
            risk_score += 0.2
        
        # Low feedback sentiment
        feedbacks = employee_data.get("feedbacks", [])
        if feedbacks:
            negative_feedback = sum(1 for f in feedbacks if f.get("type") == "negative" or f.get("rating", 3) < 3)
            if negative_feedback / len(feedbacks) > 0.3:
                risk_factors.append("Negative feedback trend")
                risk_score += 0.15
        
        risk_level = "low"
        if risk_score >= 0.6:
            risk_level = "high"
        elif risk_score >= 0.3:
            risk_level = "medium"
        
        return {
            "risk_score": min(1.0, risk_score),
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "recommendations": self._get_burnout_recommendations(risk_level, risk_factors)
        }
    
    def predict_promotion_readiness(self, employee_id: str, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict promotion readiness
        
        Factors:
        - Consistent high performance
        - Skill development
        - Leadership indicators
        - Goal achievement
        """
        readiness_score = 0.0
        factors = []
        
        # Performance factor
        performance_history = employee_data.get("performance_history", [])
        if performance_history:
            avg_performance = np.mean([p.get("performance_score", 50) for p in performance_history[-6:]])
            if avg_performance >= 80:
                factors.append("High consistent performance")
                readiness_score += 0.3
            elif avg_performance >= 70:
                readiness_score += 0.15
        
        # Goal achievement
        goals = employee_data.get("goals", [])
        if goals:
            completed_goals = len([g for g in goals if g.get("status") == "completed"])
            completion_rate = completed_goals / len(goals) if goals else 0
            if completion_rate >= 0.8:
                factors.append("High goal achievement rate")
                readiness_score += 0.25
        
        # Skill development
        skills = employee_data.get("skills", {})
        if isinstance(skills, dict):
            high_skills = sum(1 for level in skills.values() if level >= 4)
            if high_skills >= 3:
                factors.append("Strong skill set")
                readiness_score += 0.2
        
        # Leadership indicators
        # (Could check for mentoring, team leadership, etc.)
        
        readiness_level = "not_ready"
        if readiness_score >= 0.7:
            readiness_level = "ready"
        elif readiness_score >= 0.5:
            readiness_level = "almost_ready"
        
        return {
            "readiness_score": min(1.0, readiness_score),
            "readiness_level": readiness_level,
            "factors": factors,
            "recommendations": self._get_promotion_recommendations(readiness_level, factors)
        }
    
    def _get_burnout_recommendations(self, risk_level: str, factors: List[str]) -> List[str]:
        """Get recommendations for burnout prevention"""
        recommendations = []
        
        if risk_level == "high":
            recommendations.append("Immediate workload reduction recommended")
            recommendations.append("Consider time off or reduced hours")
            recommendations.append("Schedule check-in with manager")
        elif risk_level == "medium":
            recommendations.append("Monitor workload and stress levels")
            recommendations.append("Consider delegating some tasks")
        
        if "High workload" in factors:
            recommendations.append("Prioritize tasks and delegate when possible")
        if "Declining performance" in factors:
            recommendations.append("Review performance with manager")
        
        return recommendations if recommendations else ["No immediate concerns"]
    
    def _get_promotion_recommendations(self, readiness_level: str, factors: List[str]) -> List[str]:
        """Get recommendations for promotion readiness"""
        recommendations = []
        
        if readiness_level == "ready":
            recommendations.append("Employee is ready for promotion consideration")
            recommendations.append("Review promotion opportunities")
        elif readiness_level == "almost_ready":
            recommendations.append("Continue current development path")
            recommendations.append("Focus on remaining skill gaps")
        else:
            recommendations.append("Continue skill development")
            recommendations.append("Focus on consistent high performance")
        
        return recommendations

