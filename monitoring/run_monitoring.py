from monitoring.data_drift import DataDriftMonitor
from monitoring.performance import PerformanceMonitor

drift = DataDriftMonitor().compute_stats()
perf = PerformanceMonitor().ml()

print("Data snapshot:", drift)
print("Model performance:", perf)