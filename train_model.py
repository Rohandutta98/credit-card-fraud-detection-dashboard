import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

# create models folder if not exists
os.makedirs("models", exist_ok=True)

df = pd.read_csv("data/creditcard.csv")

X = df.drop("Class", axis=1)

model = IsolationForest(n_estimators=100, contamination=0.002, random_state=42)

model.fit(X)

joblib.dump(model, "models/fraud_model.pkl")

print("Model trained and saved!")