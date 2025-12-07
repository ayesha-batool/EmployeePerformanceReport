"""Limit performance data to prevent circular reference errors"""
from components.managers.data_manager import DataManager

dm = DataManager()
perf = dm.load_data('performance')

if perf:
    print(f"Current performance records: {len(perf)}")
    if len(perf) > 50:
        # Keep only the most recent 50 records
        limited = perf[-50:]  # Last 50 records (most recent)
        dm.save_data('performance', limited)
        print(f"✅ Limited performance to {len(limited)} most recent records")
    else:
        print(f"✅ Performance data is within limits ({len(perf)} records)")
else:
    print("No performance data found")

