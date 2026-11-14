
import pandas as pd

from pathlib import Path
from sqlalchemy import create_engine, text, event

# ==========================================
# 1. PROJECT CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[1]

PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
DATABASE_DIR = BASE_DIR / "database"

DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_PATH = DATABASE_DIR / "enterprise_risk_dr.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(DATABASE_URL)


# ==========================================
# 2. ENABLE FOREIGN KEY ENFORCEMENT
# ==========================================

def enable_foreign_keys(dbapi_connection, connection_record):

    cursor = dbapi_connection.cursor()

    cursor.execute("PRAGMA foreign_keys=ON")

    cursor.close()


event.listen(
    engine,
    "connect",
    enable_foreign_keys
)


# ==========================================
# 3. CREATE DATABASE TABLES
# ==========================================

create_table_queries = [

    """
    CREATE TABLE IF NOT EXISTS business_units (
        Business_Unit_ID TEXT PRIMARY KEY,
        Business_Unit_Name TEXT NOT NULL,
        Department_Head TEXT,
        Location TEXT,
        Unit_Type TEXT
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS applications (
        Application_ID TEXT PRIMARY KEY,
        Application_Name TEXT NOT NULL,
        Business_Unit_ID TEXT NOT NULL,
        Criticality TEXT,
        Application_Owner TEXT,
        Environment TEXT,
        Application_Type TEXT,
        Target_RTO_Hours REAL,
        Target_RPO_Hours REAL,
        FOREIGN KEY (Business_Unit_ID)
        REFERENCES business_units(Business_Unit_ID)
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS risk_assessments (
        Assessment_ID TEXT PRIMARY KEY,
        Application_ID TEXT NOT NULL,
        Assessment_Date TEXT,
        Threat_Type TEXT,
        Inherent_Risk_Score REAL,
        Control_Effectiveness_Percent REAL,
        Residual_Risk_Score REAL,
        Risk_Level TEXT,
        FOREIGN KEY (Application_ID)
        REFERENCES applications(Application_ID)
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS dr_assessments (
        DR_Assessment_ID TEXT PRIMARY KEY,
        Application_ID TEXT NOT NULL,
        Test_Number INTEGER,
        DR_Test_Type TEXT,
        Target_RTO_Hours REAL,
        Actual_Recovery_Time_Hours REAL,
        RTO_Status TEXT,
        Target_RPO_Hours REAL,
        Actual_Data_Loss_Hours REAL,
        RPO_Status TEXT,
        DR_Test_Result TEXT,
        FOREIGN KEY (Application_ID)
        REFERENCES applications(Application_ID)
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS incidents (
        Incident_ID TEXT PRIMARY KEY,
        Application_ID TEXT NOT NULL,
        Incident_Date TEXT,
        Incident_Type TEXT,
        Severity TEXT,
        Downtime_Hours REAL,
        Financial_Impact_INR REAL,
        DR_Activated TEXT,
        Incident_Status TEXT,
        FOREIGN KEY (Application_ID)
        REFERENCES applications(Application_ID)
    )
    """
]


# ==========================================
# 4. CREATE TABLES IN SQLITE
# ==========================================

with engine.begin() as connection:

    # Drop existing tables in dependency order
    connection.execute(text("DROP TABLE IF EXISTS incidents"))
    connection.execute(text("DROP TABLE IF EXISTS dr_assessments"))
    connection.execute(text("DROP TABLE IF EXISTS risk_assessments"))
    connection.execute(text("DROP TABLE IF EXISTS applications"))
    connection.execute(text("DROP TABLE IF EXISTS business_units"))

    # Create all five tables
    for query in create_table_queries:
        connection.execute(text(query))

print("Database tables created successfully!")


# ==========================================
# 5. LOAD PROCESSED CSV FILES
# ==========================================

datasets = {
    "business_units": "business_units.csv",
    "applications": "applications.csv",
    "risk_assessments": "risk_assessments.csv",
    "dr_assessments": "dr_assessments.csv",
    "incidents": "incidents.csv"
}

for table_name, filename in datasets.items():

    file_path = PROCESSED_DATA_DIR / filename

    df = pd.read_csv(file_path)

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="append",
        index=False
    )

    print(
        f"Loaded {len(df)} records into {table_name}"
    )


# ==========================================
# 6. VERIFY DATABASE RECORD COUNTS
# ==========================================

print("\nDATABASE RECORD COUNT")
print("-" * 40)

for table_name in datasets.keys():

    query = text(
        f"SELECT COUNT(*) FROM {table_name}"
    )

    with engine.connect() as connection:
        count = connection.execute(query).scalar()

    print(f"{table_name}: {count} records")


# ==========================================
# 7. CHECK FOREIGN KEY INTEGRITY
# ==========================================

with engine.connect() as connection:

    integrity_result = connection.execute(
        text("PRAGMA foreign_key_check")
    ).fetchall()

print("\nFOREIGN KEY VALIDATION")

if len(integrity_result) == 0:
    print("All foreign key relationships are valid.")
else:
    print("Foreign key violations detected:")
    print(integrity_result)


# ==========================================
# 8. FINAL DATABASE SUMMARY
# ==========================================

print("\n" + "=" * 60)
print("DATABASE CREATION COMPLETED")
print("=" * 60)

print("Database Location:", DATABASE_PATH)
print("Total Tables:", len(datasets))

engine.dispose()
