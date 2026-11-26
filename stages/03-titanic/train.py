"""Обучение модели (вариант A): выживет ли пассажир Титаника."""
import pickle
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).parent
FEATURES = ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare"]

df = pd.read_csv(ROOT / "data" / "titanic.csv")
X_train, X_test, y_train, y_test = train_test_split(
    df[FEATURES], df["Survived"], test_size=0.2, random_state=42, stratify=df["Survived"]
)

# Медиана считается только по обучающей выборке
age_median = float(X_train["Age"].median())


def prepare(data: pd.DataFrame) -> pd.DataFrame:
    data = data.fillna({"Age": age_median})
    return pd.get_dummies(data, columns=["Sex"], drop_first=True, dtype=int)


X_train, X_test = prepare(X_train), prepare(X_test)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
print(f"rows: {len(df)}, accuracy: {accuracy_score(y_test, model.predict(X_test)):.3f}")

with open(ROOT / "app" / "model.pkl", "wb") as f:
    pickle.dump({"model": model, "columns": list(X_train.columns), "age_median": age_median}, f)
print("saved: app/model.pkl")
