from decision.run_baseline import is_risky_baseline

def test_baseline_high_delay():
    assert is_risky_baseline(avg_days_late=20, unpaid_balance=100) is True


def test_baseline_high_unpaid_balance():
    assert is_risky_baseline(avg_days_late=5, unpaid_balance=20000) is True


def test_baseline_safe_customer():
    assert is_risky_baseline(avg_days_late=5, unpaid_balance=100) is False