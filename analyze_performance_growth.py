"""Analyze what's causing performance.json to grow"""
from components.managers.data_manager import DataManager
import json
from collections import Counter
from datetime import datetime

dm = DataManager()
perf = dm.load_data('performance') or []

print(f"Total performance records: {len(perf)}")
print(f"Unique employee IDs: {len(set(d.get('employee_id') for d in perf))}")

# Count evaluations per employee
employee_counts = Counter(d.get('employee_id') for d in perf)
print(f"\nEvaluations per employee:")
for emp_id, count in employee_counts.most_common():
    print(f"  Employee {emp_id}: {count} evaluations")

# Check for duplicate evaluations (same employee, same timestamp)
print(f"\nChecking for rapid successive evaluations...")
for emp_id in set(d.get('employee_id') for d in perf):
    emp_perf = [p for p in perf if p.get('employee_id') == emp_id]
    emp_perf.sort(key=lambda x: x.get('evaluated_at', ''))
    
    # Check for evaluations within 1 second of each other
    rapid_count = 0
    for i in range(len(emp_perf) - 1):
        try:
            time1 = datetime.fromisoformat(emp_perf[i].get('evaluated_at', ''))
            time2 = datetime.fromisoformat(emp_perf[i+1].get('evaluated_at', ''))
            if (time2 - time1).total_seconds() < 1:
                rapid_count += 1
        except:
            pass
    
    if rapid_count > 0:
        print(f"  Employee {emp_id}: {rapid_count} rapid successive evaluations (< 1 second apart)")

print(f"\nMost recent 5 evaluations:")
for p in sorted(perf, key=lambda x: x.get('evaluated_at', ''), reverse=True)[:5]:
    print(f"  Employee {p.get('employee_id')} at {p.get('evaluated_at')}")

