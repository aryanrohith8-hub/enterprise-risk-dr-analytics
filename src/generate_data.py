# ==========================================
# ENTERPRISE RISK & DR ANALYTICS PLATFORM
# Synthetic Data Generation
# ==========================================

import pandas as pd
import numpy as np
from pathlib import Path

# Ensure reproducible data generation
np.random.seed(42)

# Identify the main project directory
BASE_DIR = Path(__file__).resolve().parents[1]

# Define the raw data output directory
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

# Create the directory if it doesn't exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

print("Enterprise Risk & DR Data Generation Started")

# ==========================================
# 1. BUSINESS UNITS DATASET
# ==========================================

business_units = [
    {
        "Business_Unit_ID": "BU001",
        "Business_Unit_Name": "Finance",
        "Department_Head": "Finance Director",
        "Location": "Mumbai",
        "Unit_Type": "Business"
    },
    {
        "Business_Unit_ID": "BU002",
        "Business_Unit_Name": "Human Resources",
        "Department_Head": "HR Director",
        "Location": "Bangalore",
        "Unit_Type": "Business"
    },
    {
        "Business_Unit_ID": "BU003",
        "Business_Unit_Name": "Information Technology",
        "Department_Head": "Chief Technology Officer",
        "Location": "Hyderabad",
        "Unit_Type": "Technology"
    },
    {
        "Business_Unit_ID": "BU004",
        "Business_Unit_Name": "Operations",
        "Department_Head": "Operations Director",
        "Location": "Mumbai",
        "Unit_Type": "Business"
    },
    {
        "Business_Unit_ID": "BU005",
        "Business_Unit_Name": "Customer Experience",
        "Department_Head": "Customer Experience Head",
        "Location": "Delhi",
        "Unit_Type": "Business"
    },
    {
        "Business_Unit_ID": "BU006",
        "Business_Unit_Name": "Sales",
        "Department_Head": "Sales Director",
        "Location": "Pune",
        "Unit_Type": "Business"
    },
    {
        "Business_Unit_ID": "BU007",
        "Business_Unit_Name": "Legal and Compliance",
        "Department_Head": "Compliance Head",
        "Location": "Mumbai",
        "Unit_Type": "Control"
    },
    {
        "Business_Unit_ID": "BU008",
        "Business_Unit_Name": "Risk Management",
        "Department_Head": "Chief Risk Officer",
        "Location": "Bangalore",
        "Unit_Type": "Control"
    },
    {
        "Business_Unit_ID": "BU009",
        "Business_Unit_Name": "Supply Chain",
        "Department_Head": "Supply Chain Head",
        "Location": "Chennai",
        "Unit_Type": "Business"
    },
    {
        "Business_Unit_ID": "BU010",
        "Business_Unit_Name": "Marketing",
        "Department_Head": "Marketing Director",
        "Location": "Delhi",
        "Unit_Type": "Business"
    }
]

# Convert the list into a Pandas DataFrame
business_units_df = pd.DataFrame(business_units)

# Export the dataset to CSV
business_units_df.to_csv(
    RAW_DATA_DIR / "business_units.csv",
    index=False
)

print("\nBusiness Units Dataset Generated Successfully")
print(business_units_df.head(10))
print("Total Business Units:", len(business_units_df))
# ==========================================
# 2. APPLICATIONS DATASET
# ==========================================

# Application names belonging to each business unit

application_catalog = {
    "BU001": [
        "Payment Gateway", "Core Banking System",
        "Financial Reporting", "Payroll Processing",
        "Accounts Payable", "Tax Management",
        "Treasury Management", "Invoice Processing",
        "Budget Planning", "Expense Management"
    ],

    "BU002": [
        "Employee Portal", "Recruitment System",
        "HR Management System", "Attendance Tracker",
        "Performance Management", "Training Portal",
        "Employee Benefits", "Leave Management",
        "Talent Management", "HR Analytics"
    ],

    "BU003": [
        "Cloud Infrastructure", "Network Management",
        "Identity Management", "Database Platform",
        "IT Service Management", "Backup Management",
        "Security Monitoring", "DevOps Platform",
        "Enterprise API Gateway", "Data Warehouse"
    ],

    "BU004": [
        "Order Management", "Operations Dashboard",
        "Workflow Automation", "Process Monitoring",
        "Production Management", "Quality Control",
        "Resource Planning", "Logistics Management",
        "Facility Management", "Operations Reporting"
    ],

    "BU005": [
        "Customer CRM", "Customer Support Portal",
        "Feedback Management", "Contact Centre",
        "Customer Data Platform", "Complaint Management",
        "Loyalty Management", "Service Booking",
        "Customer Analytics", "Chatbot Platform"
    ],

    "BU006": [
        "Sales Management", "Lead Management",
        "Sales Analytics", "Partner Portal",
        "Quotation System", "Contract Management",
        "Sales Forecasting", "Order Tracking",
        "Customer Pipeline", "Commission Management"
    ],

    "BU007": [
        "Compliance Monitoring", "Legal Case Management",
        "Regulatory Reporting", "Policy Management",
        "Audit Management", "Contract Repository",
        "Data Privacy Management", "Document Control",
        "Legal Research Portal", "Compliance Tracker"
    ],

    "BU008": [
        "Enterprise Risk Platform", "Risk Assessment Tool",
        "Fraud Detection System", "Risk Reporting",
        "Business Continuity Platform", "Control Monitoring",
        "Third Party Risk System", "Incident Risk Tracker",
        "Governance Portal", "Risk Analytics"
    ],

    "BU009": [
        "Inventory Management", "Warehouse Management",
        "Supplier Management", "Procurement System",
        "Fleet Management", "Supply Chain Analytics",
        "Shipment Tracking", "Demand Forecasting",
        "Vendor Portal", "Distribution Management"
    ],

    "BU010": [
        "Marketing Analytics", "Campaign Management",
        "Social Media Platform", "Email Marketing",
        "Content Management", "Brand Monitoring",
        "Marketing Automation", "Digital Advertising",
        "Market Research Portal", "SEO Analytics"
    ]
}


# Define recovery targets based on application criticality

recovery_targets = {
    "Critical": {"RTO": 4, "RPO": 0.5},
    "High": {"RTO": 8, "RPO": 2},
    "Medium": {"RTO": 24, "RPO": 8},
    "Low": {"RTO": 72, "RPO": 24}
}


# Criticality distribution

criticality_levels = ["Critical", "High", "Medium", "Low"]

criticality_probabilities = [0.15, 0.30, 0.35, 0.20]


# Store all application records

applications = []

application_counter = 1


# Generate applications for every business unit

for bu_id, app_names in application_catalog.items():

    for app_name in app_names:

        # Assign application criticality
        criticality = np.random.choice(
            criticality_levels,
            p=criticality_probabilities
        )

        # Retrieve recovery targets
        rto = recovery_targets[criticality]["RTO"]
        rpo = recovery_targets[criticality]["RPO"]

        # Create application record
        application = {
            "Application_ID": f"APP{application_counter:03d}",
            "Application_Name": app_name,
            "Business_Unit_ID": bu_id,
            "Criticality": criticality,
            "Application_Owner": f"{business_units_df.loc[business_units_df['Business_Unit_ID'] == bu_id, 'Business_Unit_Name'].iloc[0]} IT Team",
            "Environment": np.random.choice(
                ["Production", "Staging", "Development"],
                p=[0.70, 0.20, 0.10]
            ),
            "Application_Type": np.random.choice(
                ["Web Application", "Database", "Enterprise Software", "Cloud Service"]
            ),
            "Target_RTO_Hours": rto,
            "Target_RPO_Hours": rpo
        }

        applications.append(application)

        application_counter += 1


# Convert records into a DataFrame

applications_df = pd.DataFrame(applications)


# Export applications dataset

applications_df.to_csv(
    RAW_DATA_DIR / "applications.csv",
    index=False
)


# Display results

print("\nApplications Dataset Generated Successfully")
print(applications_df.head())

print("\nTotal Applications:", len(applications_df))

print("\nCriticality Distribution:")
print(applications_df["Criticality"].value_counts())

print("\nApplications by Business Unit:")
print(applications_df["Business_Unit_ID"].value_counts())


# ==========================================
# 3. RISK ASSESSMENTS DATASET
# ==========================================

assessment_dates = pd.to_datetime([
    "2025-12-31",
    "2026-03-31",
    "2026-06-30"
])

risk_categories = ["Low", "Medium", "High", "Critical"]

threat_types = [
    "Cyberattack",
    "Data Breach",
    "System Failure",
    "Unauthorized Access",
    "Third Party Risk",
    "Data Loss"
]

risk_assessments = []

assessment_counter = 1

for _, app in applications_df.iterrows():

    # Generate an initial inherent risk score for each application
    base_inherent_risk = np.random.randint(35, 96)

    for date in assessment_dates:

        # Introduce small changes in risk over time
        inherent_risk = np.clip(
            base_inherent_risk + np.random.randint(-8, 9),
            1,
            100
        )

        # Generate control effectiveness percentage
        control_effectiveness = np.random.randint(35, 96)

        # Calculate remaining risk after controls
        residual_risk = round(
            inherent_risk *
            (1 - control_effectiveness / 100),
            2
        )

        # Classify residual risk
        if residual_risk <= 25:
            risk_level = "Low"
        elif residual_risk <= 50:
            risk_level = "Medium"
        elif residual_risk <= 75:
            risk_level = "High"
        else:
            risk_level = "Critical"

        assessment = {
            "Assessment_ID": f"RA{assessment_counter:04d}",
            "Application_ID": app["Application_ID"],
            "Assessment_Date": date,
            "Threat_Type": np.random.choice(threat_types),
            "Inherent_Risk_Score": inherent_risk,
            "Control_Effectiveness_Percent": control_effectiveness,
            "Residual_Risk_Score": residual_risk,
            "Risk_Level": risk_level
        }

        risk_assessments.append(assessment)
        assessment_counter += 1

risk_assessments_df = pd.DataFrame(risk_assessments)

risk_assessments_df.to_csv(
    RAW_DATA_DIR / "risk_assessments.csv",
    index=False
)

print("\nRisk Assessments Dataset Generated Successfully")
print(risk_assessments_df.head())

print("\nTotal Risk Assessments:", len(risk_assessments_df))

print("\nRisk Level Distribution:")
print(risk_assessments_df["Risk_Level"].value_counts())

print("\nAverage Inherent Risk Score:",
      round(risk_assessments_df["Inherent_Risk_Score"].mean(), 2))

print("Average Residual Risk Score:",
      round(risk_assessments_df["Residual_Risk_Score"].mean(), 2))


# ==========================================
# 4. DISASTER RECOVERY ASSESSMENTS DATASET
# ==========================================

dr_assessments = []

dr_counter = 1

dr_test_types = [
    "Full DR Drill",
    "Partial DR Drill",
    "Backup Restoration Test",
    "Failover Test"
]

for _, app in applications_df.iterrows():

    # Generate two DR tests for every application
    for test_number in range(1, 3):

        target_rto = app["Target_RTO_Hours"]
        target_rpo = app["Target_RPO_Hours"]

        # Generate actual recovery time
        actual_recovery_time = round(
            target_rto * np.random.uniform(0.5, 1.8), 2
        )

        # Generate actual data loss window
        actual_data_loss = round(
            target_rpo * np.random.uniform(0.3, 1.8), 2
        )

        # Check RTO and RPO compliance
        rto_status = (
            "Met" if actual_recovery_time <= target_rto
            else "Breached"
        )

        rpo_status = (
            "Met" if actual_data_loss <= target_rpo
            else "Breached"
        )

        # Overall DR test result
        dr_test_result = (
            "Passed"
            if rto_status == "Met" and rpo_status == "Met"
            else "Failed"
        )

        dr_assessment = {
            "DR_Assessment_ID": f"DR{dr_counter:04d}",
            "Application_ID": app["Application_ID"],
            "Test_Number": test_number,
            "DR_Test_Type": np.random.choice(dr_test_types),
            "Target_RTO_Hours": target_rto,
            "Actual_Recovery_Time_Hours": actual_recovery_time,
            "RTO_Status": rto_status,
            "Target_RPO_Hours": target_rpo,
            "Actual_Data_Loss_Hours": actual_data_loss,
            "RPO_Status": rpo_status,
            "DR_Test_Result": dr_test_result
        }

        dr_assessments.append(dr_assessment)
        dr_counter += 1

dr_assessments_df = pd.DataFrame(dr_assessments)

dr_assessments_df.to_csv(
    RAW_DATA_DIR / "dr_assessments.csv",
    index=False
)

print("\nDR Assessments Dataset Generated Successfully")
print(dr_assessments_df.head())

print("\nTotal DR Assessments:", len(dr_assessments_df))

print("\nDR Test Result Distribution:")
print(dr_assessments_df["DR_Test_Result"].value_counts())

print("\nRTO Compliance:")
print(dr_assessments_df["RTO_Status"].value_counts())

print("\nRPO Compliance:")
print(dr_assessments_df["RPO_Status"].value_counts())


# ==========================================
# 5. INCIDENTS DATASET
# ==========================================

incident_types = [
    "Cyberattack",
    "Server Failure",
    "Database Outage",
    "Network Disruption",
    "Data Breach",
    "Cloud Service Outage"
]

severity_levels = ["Low", "Medium", "High", "Critical"]
severity_probabilities = [0.20, 0.35, 0.30, 0.15]

incidents = []

incident_counter = 1

# Generate 150 incidents across the application portfolio
for incident_number in range(150):

    # Randomly select an affected application
    app = applications_df.sample(
        n=1,
        random_state=None
    ).iloc[0]

    severity = np.random.choice(
        severity_levels,
        p=severity_probabilities
    )

    # Downtime based on incident severity
    downtime_ranges = {
        "Low": (0.5, 3),
        "Medium": (3, 8),
        "High": (8, 24),
        "Critical": (24, 72)
    }

    downtime = round(
        np.random.uniform(*downtime_ranges[severity]), 2
    )

    # Estimate financial impact based on severity and downtime
    impact_multipliers = {
        "Low": 5000,
        "Medium": 15000,
        "High": 30000,
        "Critical": 50000
    }

    financial_impact = round(
        downtime * impact_multipliers[severity], 2
    )

    # Determine whether DR was activated
    dr_activated = np.random.choice(
        ["Yes", "No"],
        p=[0.75, 0.25]
    )

    incident = {
        "Incident_ID": f"INC{incident_counter:04d}",
        "Application_ID": app["Application_ID"],
        "Incident_Date": (
            pd.Timestamp("2025-01-01")
            + pd.Timedelta(days=int(np.random.randint(0, 365)))
        ),
        "Incident_Type": np.random.choice(incident_types),
        "Severity": severity,
        "Downtime_Hours": downtime,
        "Financial_Impact_INR": financial_impact,
        "DR_Activated": dr_activated,
        "Incident_Status": np.random.choice(
            ["Resolved", "Under Investigation", "Open"],
            p=[0.75, 0.15, 0.10]
        )
    }

    incidents.append(incident)
    incident_counter += 1

incidents_df = pd.DataFrame(incidents)

incidents_df.to_csv(
    RAW_DATA_DIR / "incidents.csv",
    index=False
)

print("\nIncidents Dataset Generated Successfully")
print(incidents_df.head())

print("\nTotal Incidents:", len(incidents_df))

print("\nIncident Severity Distribution:")
print(incidents_df["Severity"].value_counts())

print("\nDR Activation Distribution:")
print(incidents_df["DR_Activated"].value_counts())

print("\nTotal Financial Impact (INR):",
      round(incidents_df["Financial_Impact_INR"].sum(), 2))

