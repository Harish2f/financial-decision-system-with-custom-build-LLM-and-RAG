from decision.pipeline import DecisionPipeline


def test_pipeline_runs_end_to_end():
    pipeline = DecisionPipeline()

    baseline_metrics = pipeline.run_baseline()
    ml_metrics = pipeline.run_ml()

    assert "accuracy" in baseline_metrics
    assert "accuracy" in ml_metrics