import lorem
from fastapi import FastAPI

MODEL_VERSION = "v1.0"

app = FastAPI(title="Inference API", version=MODEL_VERSION)

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/infer")
def infer() -> dict:
    return {
        "model_version": MODEL_VERSION,
        "result": lorem.sentence(),
    }
