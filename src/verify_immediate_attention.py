import pandas as pd

# Load datasets
apps = pd.read_csv("data/processed/applications.csv")
risks = pd.read_csv("data/processed/risk_assessments.csv")
dr = pd.read_csv("data/processed/dr_assessments.csv")

# Get latest risk assessment for each application
latest_risks = risks[
    risks["Assessment_Date"] == "2026-06-30"
]

# Identify applications with at least one failed DR test
failed_apps = dr[
    dr["DR_Test_Result"] == "Failed"
]["Application_ID"].unique()

# Combine application and latest risk information
combined = apps.merge(
    latest_risks[["Application_ID", "Residual_Risk_Score"]],
    on="Application_ID"
)

# Apply all three conditions
priority_apps = combined[
    (combined["Criticality"].isin(["High", "Critical"])) &
    (combined["Residual_Risk_Score"] > 50) &
    (combined["Application_ID"].isin(failed_apps))
]

print("Applications with latest risk above 50:",
      len(combined[combined["Residual_Risk_Score"] > 50]))

print("High/Critical applications with risk above 50:",
      len(combined[
          (combined["Criticality"].isin(["High", "Critical"])) &
          (combined["Residual_Risk_Score"] > 50)
      ]))

print("Applications requiring immediate attention:",
      len(priority_apps))

print("\nApplication details:")
print(priority_apps[
    ["Application_ID", "Application_Name",
     "Criticality", "Residual_Risk_Score"]
].to_string(index=False))