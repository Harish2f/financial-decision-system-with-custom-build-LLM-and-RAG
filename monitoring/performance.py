from decision.pipeline import DecisionPipeline

class PerformanceMonitor:
    def baseline(self):
        return DecisionPipeline().run_baseline()

    def ml(self):
        return DecisionPipeline().run_ml()