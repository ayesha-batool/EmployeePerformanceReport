"""
Train Performance Scoring ML Model
This script trains the Random Forest/XGBoost model for performance scoring using historical data.
"""
import sys
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from components.managers.data_manager import DataManager
from components.ml.performance_scorer import PerformanceScorer


def prepare_training_data(data_manager: DataManager) -> tuple[List[Dict[str, Any]], List[float]]:
    """
    Prepare training data from historical performance records
    
    Returns:
        tuple: (training_data, target_scores)
        - training_data: List of employee data dictionaries
        - target_scores: List of actual performance scores (0-100)
    """
    print("📊 Preparing training data from Supabase...")
    
    # Load all data
    employees = data_manager.load_data("employees") or []
    tasks = data_manager.load_data("tasks") or []
    feedbacks = data_manager.load_data("feedback") or []
    performances = data_manager.load_data("performances") or []
    attendance = data_manager.load_data("attendance") or []
    
    print(f"   Found {len(employees)} employees")
    print(f"   Found {len(tasks)} tasks")
    print(f"   Found {len(feedbacks)} feedbacks")
    print(f"   Found {len(performances)} performance records")
    print(f"   Found {len(attendance)} attendance records")
    
    training_data = []
    target_scores = []
    
    # Use historical performance records as ground truth
    for perf_record in performances:
        employee_id = perf_record.get("employee_id")
        if not employee_id:
            continue
        
        # Get actual performance score from historical record
        actual_score = perf_record.get("performance_score")
        if actual_score is None or actual_score < 0 or actual_score > 100:
            continue
        
        # Get employee's tasks at the time of evaluation
        evaluated_at = perf_record.get("evaluated_at")
        if evaluated_at:
            try:
                eval_date = datetime.fromisoformat(evaluated_at.replace('Z', '+00:00'))
                # Get tasks before evaluation date
                employee_tasks = [
                    t for t in tasks 
                    if t.get("assigned_to") == employee_id and
                    (not t.get("created_at") or 
                     datetime.fromisoformat(t["created_at"].replace('Z', '+00:00')) <= eval_date)
                ]
            except:
                employee_tasks = [t for t in tasks if t.get("assigned_to") == employee_id]
        else:
            employee_tasks = [t for t in tasks if t.get("assigned_to") == employee_id]
        
        # Get employee's feedbacks
        employee_feedbacks = [
            f for f in feedbacks 
            if str(f.get("employee_id", "")) == str(employee_id)
        ]
        
        # Get employee's attendance records
        employee_attendance = [
            a for a in attendance 
            if str(a.get("employee_id", "")) == str(employee_id)
        ]
        
        # Prepare employee data dictionary
        employee_data = {
            "tasks": employee_tasks,
            "feedbacks": employee_feedbacks,
            "attendance": employee_attendance,
            "workload": len([t for t in employee_tasks if t.get("status") in ["pending", "in_progress"]])
        }
        
        training_data.append(employee_data)
        target_scores.append(float(actual_score))
    
    print(f"\n✅ Prepared {len(training_data)} training samples")
    return training_data, target_scores


def generate_synthetic_data(data_manager: DataManager, num_samples: int = 50) -> tuple[List[Dict[str, Any]], List[float]]:
    """
    Generate synthetic training data if historical data is insufficient
    This creates realistic training examples based on patterns
    """
    print(f"🔧 Generating {num_samples} synthetic training samples...")
    
    employees = data_manager.load_data("employees") or []
    tasks = data_manager.load_data("tasks") or []
    feedbacks = data_manager.load_data("feedback") or []
    
    if not employees:
        print("❌ No employees found. Cannot generate synthetic data.")
        return [], []
    
    training_data = []
    target_scores = []
    
    import random
    import numpy as np
    
    for i in range(num_samples):
        # Random employee
        employee = random.choice(employees)
        employee_id = employee.get("id")
        
        # Generate realistic task data
        num_tasks = random.randint(5, 30)
        employee_tasks = []
        completed_count = 0
        on_time_count = 0
        
        for j in range(num_tasks):
            status = random.choices(
                ["pending", "in_progress", "completed"],
                weights=[0.2, 0.3, 0.5]
            )[0]
            
            task = {
                "id": f"synth_task_{i}_{j}",
                "assigned_to": employee_id,
                "status": status,
                "priority": random.choice(["low", "medium", "high"]),
                "created_at": (datetime.now() - timedelta(days=random.randint(0, 60))).isoformat()
            }
            
            if status == "completed":
                completed_count += 1
                task["completed_at"] = (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat()
                task["due_date"] = (datetime.now() - timedelta(days=random.randint(0, 35))).isoformat()
                # 70% on-time completion
                if random.random() < 0.7:
                    on_time_count += 1
            else:
                task["due_date"] = (datetime.now() + timedelta(days=random.randint(1, 30))).isoformat()
            
            employee_tasks.append(task)
        
        # Generate feedback data
        num_feedbacks = random.randint(2, 10)
        employee_feedbacks = []
        positive_count = 0
        negative_count = 0
        
        for j in range(num_feedbacks):
            rating = random.randint(1, 5)
            feedback = {
                "id": f"synth_feedback_{i}_{j}",
                "employee_id": employee_id,
                "rating": rating,
                "type": "positive" if rating > 3 else "negative" if rating < 3 else "neutral"
            }
            employee_feedbacks.append(feedback)
            if rating > 3:
                positive_count += 1
            elif rating < 3:
                negative_count += 1
        
        # Generate attendance data
        employee_attendance = []
        for j in range(30):  # Last 30 days
            attendance = {
                "id": f"synth_attendance_{i}_{j}",
                "employee_id": employee_id,
                "status": random.choices(["present", "absent"], weights=[0.9, 0.1])[0],
                "date": (datetime.now() - timedelta(days=30-j)).isoformat()
            }
            employee_attendance.append(attendance)
        
        # Calculate expected performance score based on features
        completion_rate = completed_count / num_tasks if num_tasks > 0 else 0
        on_time_rate = on_time_count / completed_count if completed_count > 0 else 0
        
        # Task quality (0-1)
        task_quality = 0.5
        if completed_count > 0:
            task_quality = 0.5 + (on_time_count / completed_count) * 0.3
            high_priority_completed = sum(1 for t in employee_tasks 
                                        if t.get("priority") == "high" and t.get("status") == "completed")
            task_quality += min(0.2, high_priority_completed / completed_count * 0.2)
        task_quality = min(1.0, task_quality)
        
        # Feedback sentiment (0-1)
        sentiment = 0.5
        if num_feedbacks > 0:
            sentiment = 0.5 + (positive_count - negative_count) / (num_feedbacks * 2)
        sentiment = max(0.0, min(1.0, sentiment))
        
        # Attendance (0-1)
        present_count = sum(1 for a in employee_attendance if a.get("status") == "present")
        attendance_rate = present_count / len(employee_attendance) if employee_attendance else 0.95
        
        # Workload balance (0-1)
        active_tasks = len([t for t in employee_tasks if t.get("status") in ["pending", "in_progress"]])
        if active_tasks == 0:
            workload_balance = 0.3
        elif active_tasks <= 5:
            workload_balance = 0.4 + (active_tasks / 5) * 0.1
        elif active_tasks <= 10:
            workload_balance = 0.5
        elif active_tasks <= 15:
            workload_balance = 0.5 - ((active_tasks - 10) / 5) * 0.2
        else:
            workload_balance = 0.2
        
        # Calculate target score using weighted average (same as fallback)
        weights = [0.3, 0.25, 0.25, 0.2]  # task_quality, sentiment, attendance, workload
        target_score = sum([
            task_quality * weights[0],
            sentiment * weights[1],
            attendance_rate * weights[2],
            workload_balance * weights[3]
        ]) * 100
        
        # Add some noise to make it more realistic
        target_score += random.uniform(-5, 5)
        target_score = max(0.0, min(100.0, target_score))
        
        employee_data = {
            "tasks": employee_tasks,
            "feedbacks": employee_feedbacks,
            "attendance": employee_attendance,
            "workload": active_tasks
        }
        
        training_data.append(employee_data)
        target_scores.append(target_score)
    
    print(f"✅ Generated {len(training_data)} synthetic training samples")
    return training_data, target_scores


def train_model(model_type: str = "random_forest", use_synthetic: bool = False, num_synthetic: int = 100):
    """
    Train the performance scoring ML model
    
    Args:
        model_type: "random_forest" or "xgboost"
        use_synthetic: Whether to generate synthetic data if historical data is insufficient
        num_synthetic: Number of synthetic samples to generate
    """
    print("=" * 60)
    print("🚀 Training Performance Scoring ML Model")
    print("=" * 60)
    
    # Initialize data manager
    data_manager = DataManager()
    
    # Prepare training data
    training_data, target_scores = prepare_training_data(data_manager)
    
    # If not enough data, generate synthetic data
    if len(training_data) < 20 and use_synthetic:
        print(f"\n⚠️  Only {len(training_data)} historical samples found.")
        print("   Generating synthetic data to supplement training...")
        synth_data, synth_scores = generate_synthetic_data(data_manager, num_synthetic)
        training_data.extend(synth_data)
        target_scores.extend(synth_scores)
    
    if len(training_data) < 10:
        print(f"\n❌ Insufficient training data: {len(training_data)} samples")
        print("   Need at least 10 samples to train the model.")
        print("   Options:")
        print("   1. Add more performance records to Supabase")
        print("   2. Run with --use-synthetic flag to generate synthetic data")
        return False
    
    print(f"\n📈 Training with {len(training_data)} samples")
    print(f"   Model type: {model_type}")
    
    # Initialize scorer
    scorer = PerformanceScorer(model_type=model_type)
    
    # Train model
    try:
        scorer.train(training_data, target_scores)
        print("\n✅ Model training completed successfully!")
        print(f"   Model saved to: {scorer.model_path}")
        return True
    except Exception as e:
        print(f"\n❌ Error training model: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Train Performance Scoring ML Model")
    parser.add_argument(
        "--model-type",
        type=str,
        default="random_forest",
        choices=["random_forest", "xgboost"],
        help="ML model type to use"
    )
    parser.add_argument(
        "--use-synthetic",
        action="store_true",
        help="Generate synthetic training data if historical data is insufficient"
    )
    parser.add_argument(
        "--num-synthetic",
        type=int,
        default=100,
        help="Number of synthetic samples to generate (if use-synthetic is True)"
    )
    
    args = parser.parse_args()
    
    success = train_model(
        model_type=args.model_type,
        use_synthetic=args.use_synthetic,
        num_synthetic=args.num_synthetic
    )
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 Training Complete!")
        print("=" * 60)
        print("\nThe model is now ready to use.")
        print("The PerformanceAgent will automatically load this trained model.")
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("❌ Training Failed")
        print("=" * 60)
        sys.exit(1)

