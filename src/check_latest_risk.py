
import pandas as pd

df = pd.read_csv("data/processed/risk_assessments.csv")

latest = df[df["Assessment_Date"] == "2026-06-30"]

print("Records:", len(latest))
print("Average residual risk:", latest["Residual_Risk_Score"].mean())
print("Total residual risk:", latest["Residual_Risk_Score"].sum())
