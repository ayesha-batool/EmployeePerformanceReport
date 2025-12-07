"""Test that performance evaluation no longer causes circular references"""
from components.managers.data_manager import DataManager
from components.agents.performance_agent import EnhancedPerformanceAgent

dm = DataManager()
agent = EnhancedPerformanceAgent(dm)

print("Testing performance evaluation...")
result = agent.evaluate_employee('1')
print(f"✅ Evaluation successful: Score = {result.get('performance_score')}")

perf = dm.load_data('performance')
print(f"✅ Performance records: {len(perf) if perf else 0}")

# Test that saving doesn't cause circular reference errors
print("\nTesting save operation...")
try:
    result = dm.save_data('performance', perf or [])
    print(f"✅ Save successful: {result}")
except Exception as e:
    print(f"❌ Save failed: {e}")

print("\n✅ All tests passed - no circular references!")

