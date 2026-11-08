import pandas as pd

from src.train import load_data, build_pipeline

def test_dataset_can_be_loaded():
    X, y = load_data()

    assert len(X) > 0

    assert len(X.columns) == 4

    assert set(y.unique()).issubset({0, 1})

def test_pipeline_can_be_created():
    model = build_pipeline(C=1.0)

    assert model is not None

def test_model_can_be_trained():
    X, y = load_data()

    model = build_pipeline(C=1.0)

    model.fit(X, y)

    predictions = model.predict(X)

    assert len(predictions) == len(y)
