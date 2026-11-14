
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path

# ==========================================
# 1. PROJECT CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[1]

PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
FIGURES_DIR = BASE_DIR / "reports" / "figures"

FIGURES_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid")

print("=" * 60)
print("ENTERPRISE RISK & DR ANALYTICS - EDA")
print("=" * 60)


# ==========================================
# 2. LOAD DATASETS
# ==========================================

business_units_df = pd.read_csv(
    PROCESSED_DATA_DIR / "business_units.csv"
)

applications_df = pd.read_csv(
    PROCESSED_DATA_DIR / "applications.csv"
)

risk_df = pd.read_csv(
    PROCESSED_DATA_DIR / "risk_assessments.csv",
    parse_dates=["Assessment_Date"]
)

dr_df = pd.read_csv(
    PROCESSED_DATA_DIR / "dr_assessments.csv"
)

incidents_df = pd.read_csv(
    PROCESSED_DATA_DIR / "incidents.csv",
    parse_dates=["Incident_Date"]
)

print("\nAll processed datasets loaded successfully.")


# ==========================================
# 3. PORTFOLIO OVERVIEW
# ==========================================

total_business_units = len(business_units_df)
total_applications = len(applications_df)
total_risk_assessments = len(risk_df)
total_dr_tests = len(dr_df)
total_incidents = len(incidents_df)

print("\nPORTFOLIO OVERVIEW")
print("-" * 40)

print("Business Units:", total_business_units)
print("Applications:", total_applications)
print("Risk Assessments:", total_risk_assessments)
print("DR Tests:", total_dr_tests)
print("Incidents:", total_incidents)


# ==========================================
# 4. LATEST RISK ASSESSMENT PER APPLICATION
# ==========================================

latest_risk_df = (
    risk_df.sort_values("Assessment_Date")
    .groupby("Application_ID")
    .tail(1)
)

risk_analysis = latest_risk_df.merge(
    applications_df,
    on="Application_ID",
    how="left"
)

print("\nLATEST RISK ASSESSMENTS")
print("-" * 40)

print(
    risk_analysis[
        [
            "Application_ID",
            "Criticality",
            "Inherent_Risk_Score",
            "Control_Effectiveness_Percent",
            "Residual_Risk_Score"
        ]
    ].head()
)


# ==========================================
# 5. RISK ANALYSIS BY CRITICALITY
# ==========================================

risk_by_criticality = (
    risk_analysis.groupby("Criticality")
    .agg(
        Average_Inherent_Risk=(
            "Inherent_Risk_Score", "mean"
        ),
        Average_Residual_Risk=(
            "Residual_Risk_Score", "mean"
        ),
        Average_Control_Effectiveness=(
            "Control_Effectiveness_Percent", "mean"
        ),
        Application_Count=(
            "Application_ID", "nunique"
        )
    )
    .round(2)
    .reindex(["Critical", "High", "Medium", "Low"])
)

print("\nRISK ANALYSIS BY CRITICALITY")
print(risk_by_criticality)


# ==========================================
# 6. DR COMPLIANCE ANALYSIS
# ==========================================

dr_analysis = dr_df.merge(
    applications_df,
    on="Application_ID",
    how="left"
)

rto_compliance = (
    dr_analysis["RTO_Status"].eq("Met").mean() * 100
)

rpo_compliance = (
    dr_analysis["RPO_Status"].eq("Met").mean() * 100
)

dr_pass_rate = (
    dr_analysis["DR_Test_Result"].eq("Passed").mean() * 100
)

print("\nDR COMPLIANCE")
print("-" * 40)

print("RTO Compliance:", round(rto_compliance, 2), "%")
print("RPO Compliance:", round(rpo_compliance, 2), "%")
print("Overall DR Pass Rate:", round(dr_pass_rate, 2), "%")


# ==========================================
# 7. INCIDENT ANALYSIS
# ==========================================

incident_analysis = (
    incidents_df.groupby("Severity")
    .agg(
        Total_Incidents=(
            "Incident_ID", "count"
        ),
        Average_Downtime=(
            "Downtime_Hours", "mean"
        ),
        Total_Financial_Impact=(
            "Financial_Impact_INR", "sum"
        )
    )
    .round(2)
    .reindex(["Critical", "High", "Medium", "Low"])
)

print("\nINCIDENT ANALYSIS BY SEVERITY")
print(incident_analysis)


# ==========================================
# 8. SAVE ANALYTICAL SUMMARIES
# ==========================================

risk_by_criticality.to_csv(
    PROCESSED_DATA_DIR / "risk_summary.csv"
)

incident_analysis.to_csv(
    PROCESSED_DATA_DIR / "incident_summary.csv"
)

print("\nAnalytical summaries saved successfully.")


# ==========================================
# 9. DATA VISUALISATION
# ==========================================

print("\nGenerating analytical visualisations...")

# ------------------------------------------
# CHART 1: APPLICATIONS BY CRITICALITY
# ------------------------------------------

criticality_order = ["Critical", "High", "Medium", "Low"]

application_counts = (
    applications_df["Criticality"]
    .value_counts()
    .reindex(criticality_order)
)

plt.figure(figsize=(9, 5))

application_counts.plot(
    kind="bar",
    edgecolor="black"
)

plt.title("Application Distribution by Criticality")
plt.xlabel("Application Criticality")
plt.ylabel("Number of Applications")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "applications_by_criticality.png",
    dpi=300
)

plt.show()
plt.close()


# ------------------------------------------
# CHART 2: AVERAGE RESIDUAL RISK
# ------------------------------------------

residual_risk = (
    risk_analysis.groupby("Criticality")[
        "Residual_Risk_Score"
    ]
    .mean()
    .reindex(criticality_order)
)

plt.figure(figsize=(9, 5))

residual_risk.plot(
    kind="bar",
    edgecolor="black"
)

plt.title("Average Residual Risk by Criticality")
plt.xlabel("Application Criticality")
plt.ylabel("Average Residual Risk Score")
plt.xticks(rotation=0)
plt.ylim(0, 100)
plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "residual_risk_by_criticality.png",
    dpi=300
)

plt.show()
plt.close()


# ------------------------------------------
# CHART 3: RTO AND RPO COMPLIANCE
# ------------------------------------------

compliance_data = pd.Series({
    "RTO Compliance": rto_compliance,
    "RPO Compliance": rpo_compliance,
    "Overall DR Pass Rate": dr_pass_rate
})

plt.figure(figsize=(9, 5))

compliance_data.plot(
    kind="bar",
    edgecolor="black"
)

plt.title("Disaster Recovery Compliance Overview")
plt.xlabel("Compliance Metric")
plt.ylabel("Compliance Percentage (%)")
plt.xticks(rotation=0)
plt.ylim(0, 100)
plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "dr_compliance.png",
    dpi=300
)

plt.show()
plt.close()


# ------------------------------------------
# CHART 4: INCIDENT DISTRIBUTION
# ------------------------------------------

incident_counts = (
    incidents_df["Severity"]
    .value_counts()
    .reindex(criticality_order)
)

plt.figure(figsize=(9, 5))

incident_counts.plot(
    kind="bar",
    edgecolor="black"
)

plt.title("Incident Distribution by Severity")
plt.xlabel("Incident Severity")
plt.ylabel("Number of Incidents")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "incident_distribution.png",
    dpi=300
)

plt.show()
plt.close()


# ------------------------------------------
# CHART 5: FINANCIAL IMPACT BY SEVERITY
# ------------------------------------------

financial_impact = (
    incidents_df.groupby("Severity")[
        "Financial_Impact_INR"
    ]
    .sum()
    .reindex(criticality_order)
    / 100000
)

plt.figure(figsize=(9, 5))

financial_impact.plot(
    kind="bar",
    edgecolor="black"
)

plt.title("Financial Impact by Incident Severity")
plt.xlabel("Incident Severity")
plt.ylabel("Financial Impact (INR Lakhs)")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "financial_impact_by_severity.png",
    dpi=300
)

plt.show()
plt.close()


# ==========================================
# 10. VISUALISATION SUMMARY
# ==========================================

print("\nAll visualisations generated successfully!")

print("\nCharts saved in:", FIGURES_DIR)

print("\nGenerated chart files:")

for chart_file in FIGURES_DIR.glob("*.png"):
    print("-", chart_file.name)
