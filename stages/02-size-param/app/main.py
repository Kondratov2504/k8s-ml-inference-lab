from typing import Literal

import lorem
from fastapi import FastAPI

MODEL_VERSION = "v2.0"

app = FastAPI(title="Inference API", version=MODEL_VERSION)

GENERATORS = {
    "sentence": lorem.sentence,
    "paragraph": lorem.paragraph,
    "text": lorem.text,
}


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/infer")
def infer(size: Literal["sentence", "paragraph", "text"] = "sentence") -> dict:
    return {
        "model_version": MODEL_VERSION,
        "size": size,
        "result": GENERATORS[size](),
    }