# api.py
# ------------------------------------------------------------
# FastAPI API für Random Forest Blutbild-Klassifikation
# ------------------------------------------------------------

import pandas as pd
import numpy as np
from fastapi import FastAPI
from pydantic import create_model
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# ------------------------------------------------------------
# 1. Daten laden und Modell einmalig trainieren
# ------------------------------------------------------------
df = pd.read_csv("Datasets/diagnosed_cbc_data_v4.csv")

# Features und Zielvariable
X = df.drop("Diagnosis", axis=1)
y = df["Diagnosis"]

# Skalieren
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train/Test-Split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# Random Forest Modell
rf = RandomForestClassifier(
    n_estimators=100,
    max_depth=5,
    random_state=42
)

# Optional: Cross-Validation
kf = KFold(n_splits=3, shuffle=True, random_state=42)
cv_scores = cross_val_score(rf, X_scaled, y, cv=kf, scoring='accuracy')
print("CV Accuracy:", cv_scores.mean())

# Train final
rf.fit(X_train, y_train)

# ------------------------------------------------------------
# 2. FastAPI App
# ------------------------------------------------------------
app = FastAPI(title="CBC Diagnosis API")


# ------------------------------------------------------------
# 3. Dynamisches Input-Modell basierend auf Spalten
# ------------------------------------------------------------
fields = {col: (float, ...) for col in X.columns}
CBCInput = create_model("CBCInput", **fields)


# ------------------------------------------------------------
# 4. Prediction Endpoint
# ------------------------------------------------------------
@app.post("/predict")
def predict(input_data: CBCInput):
    """Nimmt Blutwerte entgegen und gibt die Diagnose zurück."""

    # Input → DataFrame
    df_input = pd.DataFrame([input_data.dict()])

    # Skalieren
    df_scaled = scaler.transform(df_input)

    # Vorhersage
    prediction = rf.predict(df_scaled)[0]

    # Nur Klassifikation zurückgeben
    return {"diagnosis": str(prediction)}
