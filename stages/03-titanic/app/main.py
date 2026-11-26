import pickle
from pathlib import Path
from typing import Literal, Optional

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

MODEL_VERSION = "v3.0"
VARIANT = "titanic"

with open(Path(__file__).parent / "model.pkl", "rb") as f:
    bundle = pickle.load(f)

app = FastAPI(title="Titanic Inference API", version=MODEL_VERSION)


class Passenger(BaseModel):
    Pclass: Literal[1, 2, 3]
    Sex: Literal["male", "female"]
    Age: Optional[float] = Field(default=None, ge=0, le=120)
    SibSp: int = Field(ge=0)
    Parch: int = Field(ge=0)
    Fare: float = Field(ge=0)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/predict")
def predict(p: Passenger) -> dict:
    row = {
        "Pclass": p.Pclass,
        "Age": bundle["age_median"] if p.Age is None else p.Age,
        "SibSp": p.SibSp,
        "Parch": p.Parch,
        "Fare": p.Fare,
        "Sex_male": int(p.Sex == "male"),
    }
    X = pd.DataFrame([row])[bundle["columns"]]
    probability = float(bundle["model"].predict_proba(X)[0, 1])
    return {
        "model_version": MODEL_VERSION,
        "variant": VARIANT,
        "survival_probability": round(probability, 2),
        "survived": probability >= 0.5,
    }
