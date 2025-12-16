# Training the Performance Scoring ML Model

This guide explains how to train the ML model (Option A) for performance scoring in your project.

## Overview

The Performance Scoring model uses **Random Forest** or **XGBoost** to predict employee performance scores (0-100) based on:
1. **Task Quality** - On-time completion, priority handling
2. **Feedback Sentiment** - Positive/negative feedback ratio
3. **Attendance Trend** - Recent attendance rate
4. **Workload Balance** - Optimal task distribution

## Prerequisites

### 1. Install ML Dependencies

```bash
pip install -r requirements_ml.txt
```

Or install individually:
```bash
pip install scikit-learn numpy pandas xgboost
```

### 2. Ensure You Have Training Data

The model needs historical performance records from Supabase. You need:
- **At least 10 performance records** in the `performances` table
- Each record should have a `performance_score` (0-100)
- Associated tasks, feedbacks, and attendance data

## Training Methods

### Method 1: Train with Historical Data (Recommended)

If you have historical performance records in Supabase:

```bash
python train_performance_model.py --model-type random_forest
```

Or with XGBoost:
```bash
python train_performance_model.py --model-type xgboost
```

### Method 2: Train with Synthetic Data

If you don't have enough historical data, generate synthetic training samples:

```bash
python train_performance_model.py --model-type random_forest --use-synthetic --num-synthetic 100
```

This will:
- Use any existing historical data
- Generate 100 synthetic samples based on realistic patterns
- Train the model on the combined dataset

## How It Works

### Step 1: Data Collection

The script collects data from Supabase:
- **Employees** - Employee information
- **Tasks** - All task records
- **Feedbacks** - Feedback records
- **Performances** - Historical performance evaluations
- **Attendance** - Attendance records

### Step 2: Feature Extraction

For each historical performance record, it extracts:
- Task quality metrics
- Feedback sentiment
- Attendance trends
- Workload balance

### Step 3: Model Training

1. **Feature Scaling** - Normalizes features using StandardScaler
2. **Train/Test Split** - 80% training, 20% testing
3. **Model Training** - Trains Random Forest or XGBoost
4. **Evaluation** - Calculates MSE and R² score
5. **Model Saving** - Saves to `models/performance_scorer.pkl`

### Step 4: Model Usage

Once trained, the model is automatically loaded by `PerformanceAgent`:
- Checks if model exists at `models/performance_scorer.pkl`
- If found, uses ML predictions
- If not found, falls back to weighted average calculation

## Training Output

After training, you'll see:

```
✅ Model trained. MSE: 45.23, R²: 0.87
✅ Model saved to models/performance_scorer.pkl
```

**Metrics Explained:**
- **MSE (Mean Squared Error)**: Lower is better (measures prediction error)
- **R² (R-squared)**: Higher is better (0-1, measures model fit)
  - 0.8+ = Excellent
  - 0.6-0.8 = Good
  - <0.6 = Needs improvement

## Model Configuration

### Random Forest (Default)
- **n_estimators**: 100 trees
- **max_depth**: 10 levels
- **Pros**: Fast, interpretable, handles non-linear relationships
- **Cons**: Can overfit with small datasets

### XGBoost
- **n_estimators**: 100 trees
- **max_depth**: 6 levels
- **learning_rate**: 0.1
- **Pros**: Often more accurate, handles complex patterns
- **Cons**: Slower training, requires more data

## Verifying Model Training

### Check if Model Exists

```python
import os
if os.path.exists("models/performance_scorer.pkl"):
    print("✅ Model is trained and ready!")
else:
    print("❌ Model not found. Run training script first.")
```

### Test Model Prediction

```python
from components.ml.performance_scorer import PerformanceScorer
from components.managers.data_manager import DataManager

# Load model
scorer = PerformanceScorer(model_type="random_forest")

# Check if trained
if scorer.is_trained:
    print("✅ Model is trained")
    
    # Test prediction
    test_data = {
        "tasks": [...],  # Employee tasks
        "feedbacks": [...],  # Employee feedbacks
        "attendance": [...],  # Attendance records
        "workload": 5  # Active tasks
    }
    
    score = scorer.predict(test_data)
    print(f"Predicted performance score: {score:.2f}")
else:
    print("❌ Model not trained")
```

## Troubleshooting

### Error: "scikit-learn not available"
```bash
pip install scikit-learn
```

### Error: "Insufficient training data"
**Solution 1**: Add more performance records to Supabase
```sql
-- Example: Insert performance record
INSERT INTO performances (employee_id, performance_score, evaluated_at)
VALUES ('emp_123', 85.5, NOW());
```

**Solution 2**: Use synthetic data
```bash
python train_performance_model.py --use-synthetic --num-synthetic 200
```

### Error: "XGBoost not available"
```bash
pip install xgboost
```

Or use Random Forest instead:
```bash
python train_performance_model.py --model-type random_forest
```

### Low R² Score (<0.6)
**Possible causes:**
1. Not enough training data (need 50+ samples)
2. Data quality issues (missing or incorrect values)
3. Model needs tuning

**Solutions:**
- Collect more historical data
- Use synthetic data to supplement
- Try XGBoost instead of Random Forest
- Check data quality in Supabase

## Retraining the Model

To retrain with new data:

1. **Delete old model** (optional):
   ```bash
   rm models/performance_scorer.pkl
   ```

2. **Run training again**:
   ```bash
   python train_performance_model.py --model-type random_forest
   ```

The model will be retrained with all available data, including new records.

## Integration with Performance Agent

The `PerformanceAgent` automatically uses the trained model:

```python
# In performance_agent.py
self.ml_scorer = PerformanceScorer(model_type="random_forest")

# When evaluating employee
performance_score = self.ml_scorer.predict(employee_data)

# If model not trained, falls back to:
# 1. AI fallback (if AI enabled)
# 2. Weighted average calculation
```

## Best Practices

1. **Regular Retraining**: Retrain monthly or quarterly with new data
2. **Data Quality**: Ensure performance records are accurate
3. **Feature Monitoring**: Track if features are changing over time
4. **Model Validation**: Test predictions against actual outcomes
5. **Backup Models**: Keep previous model versions for rollback

## Example Training Session

```bash
$ python train_performance_model.py --model-type random_forest --use-synthetic

============================================================
🚀 Training Performance Scoring ML Model
============================================================
📊 Preparing training data from Supabase...
   Found 25 employees
   Found 150 tasks
   Found 80 feedbacks
   Found 12 performance records
   Found 200 attendance records

✅ Prepared 12 training samples

⚠️  Only 12 historical samples found.
   Generating synthetic data to supplement training...
🔧 Generating 100 synthetic training samples...
✅ Generated 100 synthetic training samples

📈 Training with 112 samples
   Model type: random_forest
✅ Model trained. MSE: 42.15, R²: 0.89
✅ Model saved to: models/performance_scorer.pkl

============================================================
🎉 Training Complete!
============================================================

The model is now ready to use.
The PerformanceAgent will automatically load this trained model.
```

## Next Steps

After training:
1. ✅ Model is saved and ready to use
2. ✅ PerformanceAgent will automatically load it
3. ✅ All performance evaluations will use ML predictions
4. ✅ Monitor model performance over time
5. ✅ Retrain periodically with new data

