
import os

import mlflow
import mlflow.pyfunc
import pandas as pd

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


# Konfigurasi MLflow Tracking Server
MLFLOW_TRACKING_URI = os.getenv(
    "MLFLOW_TRACKING_URI",
    "http://mlflow-server:5000",
)

MODEL_URI = os.getenv(
    "MODEL_URI",
    "models:/GlobalLocalNewsModel@champion",
)

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)


# Inisialisasi FastAPI
app = FastAPI(
    title="GlobalLocalNews Prediction API",
    description="API prediksi peningkatan perhatian media Indonesia terhadap isu global.",
    version="1.0.0",
)


# Menyimpan model setelah berhasil dimuat
model = None


# Struktur input prediksi
class PredictionInput(BaseModel):
    global_growth: float
    indonesia_growth: float
    global_indonesia_ratio: float | None = None
    topic: str = Field(min_length=1)


def load_model():
    global model

    if model is None:
        model = mlflow.pyfunc.load_model(MODEL_URI)

    return model


# Endpoint utama
@app.get("/")
def home():
    return {
        "message": "GlobalLocalNews Prediction API",
        "status": "running",
    }


# Endpoint pemeriksaan kesehatan
@app.get("/health")
def health():
    try:
        load_model()

        return {
            "status": "healthy",
            "api": "running",
            "mlflow": "connected",
            "model": MODEL_URI,
        }

    except Exception as e:
        return {
            "status": "degraded",
            "api": "running",
            "mlflow": "unavailable",
            "detail": str(e),
        }


# Endpoint prediksi
@app.post("/predict")
def predict(data: PredictionInput):
    try:
        loaded_model = load_model()

        input_data = pd.DataFrame([
            {
                "global_growth": data.global_growth,
                "indonesia_growth": data.indonesia_growth,
                "global_indonesia_ratio": data.global_indonesia_ratio,
                "topic": data.topic,
            }
        ])

        prediction = loaded_model.predict(input_data)

        return {
            "prediction": int(prediction[0]),
            "label": (
                "Peningkatan perhatian media"
                if int(prediction[0]) == 1
                else "Tidak terjadi peningkatan perhatian media"
            ),
            "model": MODEL_URI,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
