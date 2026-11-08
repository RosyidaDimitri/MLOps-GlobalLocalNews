
import sys
import yaml
import mlflow

from mlflow.tracking import MlflowClient


EXPERIMENT_NAME = "LK-06-Global-vs-Local-News"
MODEL_NAME = "GlobalLocalNewsClassifier"


def main():
    with open("config/evaluation_thresholds.yaml") as file:
        config = yaml.safe_load(file)

    threshold = config["evaluation"]["minimum_f1"]

    client = MlflowClient()

    experiment = client.get_experiment_by_name(
        EXPERIMENT_NAME
    )

    if experiment is None:
        raise RuntimeError("Eksperimen MLflow tidak ditemukan.")

    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["attributes.start_time DESC"],
        max_results=1,
    )

    if not runs:
        raise RuntimeError("Tidak ditemukan hasil training.")

    run = runs[0]
    f1 = run.data.metrics.get("f1")

    if f1 is None:
        raise RuntimeError("Metrik F1 tidak ditemukan.")

    print(f"F1-score model baru : {f1:.4f}")
    print(f"Threshold minimum   : {threshold:.4f}")

    if f1 < threshold:
        print("VALIDASI GAGAL: Model tidak memenuhi threshold.")
        sys.exit(1)

    print("VALIDASI BERHASIL: Model memenuhi threshold.")

    model_uri = f"runs:/{run.info.run_id}/model"

    registered_model = mlflow.register_model(
        model_uri=model_uri,
        name=MODEL_NAME,
    )

    client.transition_model_version_stage(
        name=MODEL_NAME,
        version=registered_model.version,
        stage="Staging",
        archive_existing_versions=False,
    )

    print(f"Model berhasil didaftarkan: {MODEL_NAME}")
    print(f"Version: {registered_model.version}")
    print("Stage: Staging")


if __name__ == "__main__":
    main()
