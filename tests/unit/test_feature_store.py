from decision.feature_store import FeatureStore


def test_feature_store_schema_stability():
    store = FeatureStore()

    prod = store.load_features()
    ref = store.load_reference_features()

    assert set(prod.columns) == set(ref.columns)