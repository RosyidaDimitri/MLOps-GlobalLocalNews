
import mlflow
import mlflow.sklearn
import pandas as pd

from mlflow import MlflowClient
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.model_selection import train_test_split

from src.train import load_data, build_pipeline


# Konfigurasi MLflow
MLFLOW_TRACKING_URI = "http://mlflow-server:5000"
EXPERIMENT_NAME = "LK-09-GlobalLocalNews"
MODEL_NAME = "GlobalLocalNewsModel"

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)


def register_model():

    # Mengambil dataset dan membagi data training/testing
    X, y = load_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    # Membuat pipeline Logistic Regression
    model = build_pipeline(C=1.0)

    # Mengatur experiment MLflow
    mlflow.set_experiment(EXPERIMENT_NAME)

    with mlflow.start_run() as run:

        # Training model
        model.fit(X_train, y_train)

        # Evaluasi model
        predictions = model.predict(X_test)

        accuracy = accuracy_score(y_test, predictions)
        precision = precision_score(
            y_test, predictions, zero_division=0
        )
        recall = recall_score(
            y_test, predictions, zero_division=0
        )
        f1 = f1_score(
            y_test, predictions, zero_division=0
        )

        # Logging parameter
        mlflow.log_param("model", "LogisticRegression")
        mlflow.log_param("C", 1.0)
        mlflow.log_param("max_iter", 1000)
        mlflow.log_param("class_weight", "balanced")
        mlflow.log_param("random_state", 42)
        mlflow.log_param("test_size", 0.25)

        # Logging metrics
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1", f1)

        # Logging model sekaligus registrasi
        model_info = mlflow.sklearn.log_model(
            model,
            name="model",
            registered_model_name=MODEL_NAME,
            skops_trusted_types=["numpy.dtype"],
        )

        # Mengatur alias champion
        client = MlflowClient()

        latest_versions = client.search_model_versions(
            f"name='{MODEL_NAME}'"
        )

        latest_version = max(
            latest_versions,
            key=lambda version: int(version.version),
        )

        client.set_registered_model_alias(
            MODEL_NAME,
            "champion",
            latest_version.version,
        )

        print("\n=== HASIL REGISTRASI MODEL ===")
        print(f"Run ID       : {run.info.run_id}")
        print(f"Model URI    : {model_info.model_uri}")
        print(f"Model Name   : {MODEL_NAME}")
        print(f"Model Version: {latest_version.version}")
        print(f"Accuracy     : {accuracy:.4f}")
        print(f"Precision    : {precision:.4f}")
        print(f"Recall       : {recall:.4f}")
        print(f"F1-score     : {f1:.4f}")
        print("Alias        : champion")


if __name__ == "__main__":
    register_model()
