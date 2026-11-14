
import pandas as pd
from pathlib import Path

# ==========================================
# 1. PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[1]

RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("ENTERPRISE RISK & DR DATA CLEANING")
print("=" * 60)


# ==========================================
# 2. LOAD ALL FIVE DATASETS
# ==========================================

datasets = {
    "business_units": "business_units.csv",
    "applications": "applications.csv",
    "risk_assessments": "risk_assessments.csv",
    "dr_assessments": "dr_assessments.csv",
    "incidents": "incidents.csv"
}

dataframes = {}

for dataset_name, filename in datasets.items():

    file_path = RAW_DATA_DIR / filename

    df = pd.read_csv(file_path)

    dataframes[dataset_name] = df

    print(f"\nLoaded {dataset_name}: {len(df)} records")


# ==========================================
# 3. STANDARDIZE DATE COLUMNS
# ==========================================

date_columns = {
    "risk_assessments": ["Assessment_Date"],
    "incidents": ["Incident_Date"]
}

for dataset_name, columns in date_columns.items():

    df = dataframes[dataset_name]

    for column in columns:
        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )


# ==========================================
# 4. REMOVE DUPLICATE PRIMARY IDs
# ==========================================

primary_keys = {
    "business_units": "Business_Unit_ID",
    "applications": "Application_ID",
    "risk_assessments": "Assessment_ID",
    "dr_assessments": "DR_Assessment_ID",
    "incidents": "Incident_ID"
}

duplicate_counts = {}

for dataset_name, primary_key in primary_keys.items():

    df = dataframes[dataset_name]

    duplicate_count = df.duplicated(
        subset=[primary_key]
    ).sum()

    duplicate_counts[dataset_name] = duplicate_count

    dataframes[dataset_name] = df.drop_duplicates(
        subset=[primary_key],
        keep="first"
    )

    print(
        f"\n{dataset_name}: "
        f"{duplicate_count} duplicate IDs found"
    )


# ==========================================
# 5. CHECK MISSING VALUES
# ==========================================

missing_value_counts = {}

for dataset_name, df in dataframes.items():

    missing_count = df.isnull().sum().sum()

    missing_value_counts[dataset_name] = missing_count

    print(
        f"\n{dataset_name}: "
        f"{missing_count} missing values"
    )


# ==========================================
# 6. CHECK REFERENTIAL INTEGRITY
# ==========================================

business_unit_ids = set(
    dataframes["business_units"]["Business_Unit_ID"]
)

application_ids = set(
    dataframes["applications"]["Application_ID"]
)

invalid_business_unit_links = (
    ~dataframes["applications"]["Business_Unit_ID"]
    .isin(business_unit_ids)
).sum()

print(
    "\nInvalid Business Unit References:",
    invalid_business_unit_links
)

application_link_checks = [
    "risk_assessments",
    "dr_assessments",
    "incidents"
]

for dataset_name in application_link_checks:

    invalid_links = (
        ~dataframes[dataset_name]["Application_ID"]
        .isin(application_ids)
    ).sum()

    print(
        f"Invalid Application References "
        f"in {dataset_name}: {invalid_links}"
    )

    if invalid_links > 0:
        raise ValueError(
            f"Invalid Application_ID references in {dataset_name}"
        )

if invalid_business_unit_links > 0:
    raise ValueError(
        "Invalid Business_Unit_ID references in applications"
    )


# ==========================================
# 7. VALIDATE BUSINESS RULES
# ==========================================

risk_df = dataframes["risk_assessments"]
dr_df = dataframes["dr_assessments"]
app_df = dataframes["applications"]
incident_df = dataframes["incidents"]

invalid_risk_scores = (
    ~risk_df["Inherent_Risk_Score"].between(0, 100)
).sum()

invalid_residual_scores = (
    ~risk_df["Residual_Risk_Score"].between(0, 100)
).sum()

invalid_control_scores = (
    ~risk_df["Control_Effectiveness_Percent"].between(0, 100)
).sum()

invalid_rto = (
    (app_df["Target_RTO_Hours"] <= 0)
    | (dr_df["Target_RTO_Hours"] <= 0)
).sum()

invalid_rpo = (
    (app_df["Target_RPO_Hours"] <= 0)
    | (dr_df["Target_RPO_Hours"] <= 0)
).sum()

invalid_downtime = (
    (incident_df["Downtime_Hours"] < 0)
).sum()

invalid_financial_impact = (
    (incident_df["Financial_Impact_INR"] < 0)
).sum()

print("\nBUSINESS RULE VALIDATION")
print("-" * 40)

print("Invalid Inherent Risk Scores:", invalid_risk_scores)
print("Invalid Residual Risk Scores:", invalid_residual_scores)
print("Invalid Control Effectiveness Scores:", invalid_control_scores)
print("Invalid RTO Values:", invalid_rto)
print("Invalid RPO Values:", invalid_rpo)
print("Invalid Downtime Values:", invalid_downtime)
print("Invalid Financial Impact Values:", invalid_financial_impact)


# ==========================================
# 8. GENERATE DATA QUALITY REPORT
# ==========================================

quality_report = []

for dataset_name, df in dataframes.items():

    quality_report.append({
        "Dataset": dataset_name,
        "Total_Records": len(df),
        "Total_Columns": len(df.columns),
        "Duplicate_IDs_Removed": duplicate_counts[dataset_name],
        "Missing_Values": df.isnull().sum().sum()
    })

quality_report_df = pd.DataFrame(quality_report)

quality_report_df.to_csv(
    PROCESSED_DATA_DIR / "data_quality_report.csv",
    index=False
)


# ==========================================
# 9. SAVE CLEANED DATASETS
# ==========================================

for dataset_name, df in dataframes.items():

    output_path = (
        PROCESSED_DATA_DIR / f"{dataset_name}.csv"
    )

    df.to_csv(output_path, index=False)

    print(
        f"\nCleaned dataset saved: {output_path.name}"
    )


# ==========================================
# 10. FINAL SUMMARY
# ==========================================

print("\n" + "=" * 60)
print("DATA CLEANING COMPLETED")
print("=" * 60)

for dataset_name, df in dataframes.items():

    print(f"{dataset_name}: {len(df)} records")

print("\nData quality report saved successfully.")
print("All processed datasets are available in data/processed/")
