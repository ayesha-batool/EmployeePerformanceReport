# Quick Start: Train ML Model for Performance Scoring

## 🚀 Quick Steps

### 1. Install Dependencies
```bash
pip install scikit-learn numpy pandas xgboost
```

### 2. Train the Model
```bash
# Option A: With historical data (if you have performance records)
python train_performance_model.py

# Option B: With synthetic data (if you don't have enough historical data)
python train_performance_model.py --use-synthetic --num-synthetic 100
```

### 3. Verify Training
The model will be saved to `models/performance_scorer.pkl`

### 4. Use the Model
The `PerformanceAgent` will automatically use the trained model for all performance evaluations!

## 📋 What Happens?

1. **Data Collection**: Script reads from Supabase (tasks, feedbacks, performances, attendance)
2. **Feature Extraction**: Extracts 4 features per employee:
   - Task Quality (0-1)
   - Feedback Sentiment (0-1)
   - Attendance Rate (0-1)
   - Workload Balance (0-1)
3. **Model Training**: Trains Random Forest/XGBoost on historical data
4. **Model Saving**: Saves to `models/performance_scorer.pkl`
5. **Auto-Loading**: PerformanceAgent automatically loads and uses the model

## ✅ Success Indicators

After training, you should see:
```
✅ Model trained. MSE: XX.XX, R²: 0.XX
✅ Model saved to models/performance_scorer.pkl
```

**Good R² scores:**
- 0.8+ = Excellent ✅
- 0.6-0.8 = Good ✅
- <0.6 = Needs more data ⚠️

## 🔄 Retraining

To retrain with new data:
```bash
python train_performance_model.py --model-type random_forest
```

## 📚 Full Documentation

See `TRAIN_ML_MODEL.md` for detailed documentation.

