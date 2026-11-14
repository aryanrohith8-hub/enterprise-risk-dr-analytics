
# Enterprise Risk & Disaster Recovery Analytics

## Project Overview

An end-to-end enterprise IT risk and disaster recovery analytics project built using Python, SQL, SQLite, and Microsoft Power BI.

The project simulates an enterprise environment to evaluate application risk exposure, disaster recovery readiness, recovery objective breaches, operational incidents, and financial impact.

The objective is to transform risk and recovery assessment data into actionable management insights.

**Note:** This project uses synthetic data generated for educational and portfolio purposes. All findings are simulated.

## Technology Stack

- Python: Data generation, processing, and validation
- Pandas and NumPy: Data analysis
- SQLite and SQL: Data storage, querying, and analysis
- Power BI: Interactive management dashboard
- VS Code: Development environment

## Dataset Overview

| Dataset | Records |
|---|---:|
| Business Units | 10 |
| Applications | 100 |
| Risk Assessments | 300 |
| DR Assessments | 200 |
| Incidents | 150 |
| **Total** | **760** |

## Key Performance Indicators

| KPI | Result |
|---|---:|
| Total Applications | 100 |
| Critical & High Applications | 45 |
| Average Latest Residual Risk | 22.10 |
| RTO Breaches | 131 |
| RPO Breaches | 106 |
| Total Incidents | 150 |
| Total Incident Financial Impact | INR 71.64 Million |

The latest residual risk figure is based on assessments dated June 30, 2026.

## Key Analytical Findings

### 1. Enterprise Risk Exposure

Operations recorded the highest average latest residual risk score (31.02), followed by Information Technology (30.88).

The Business Continuity Platform had the highest individual latest residual risk score (53.12).

### 2. Disaster Recovery Performance

- 65.5% of DR assessments breached their RTO targets.
- 53% of DR assessments breached their RPO targets.
- High-criticality applications had the highest RTO breach rate (68.18%) and RPO breach rate (59.09%).

### 3. Repeated Recovery Failures

Several applications experienced both RTO and RPO breaches across two DR tests.

Examples include:
- Commission Management
- Contract Repository
- Enterprise Risk Platform
- Fraud Detection System

These findings indicate potential recovery capability weaknesses requiring further investigation.

### 4. Incident Financial Impact

The simulated incident dataset contains 150 incidents with a combined recorded financial impact of approximately INR 71.64 million.

## Management Recommendations

1. Prioritize DR remediation for business-critical applications.
2. Investigate repeated RTO and RPO breaches.
3. Review backup frequency, replication reliability, and recovery procedures.
4. Improve DR testing and track remediation outcomes.
5. Review applications with elevated residual risk scores.
6. Strengthen risk-based monitoring and management reporting.

## Data Quality and Validation

Validation checks confirmed:

- Expected record counts across all five datasets
- No duplicate identifiers
- No missing values
- No invalid application or business unit references
- No identified business-rule violations in the generated datasets

## Power BI Dashboard

The interactive management dashboard includes:

- Enterprise risk and DR performance KPIs
- Application criticality analysis
- Incident severity distribution
- Business unit and criticality slicers
- Financial impact reporting

Dashboard file: `dashboard/Enterprise_Risk_DR_Dashboard.pbix`

## Project Structure

```text
enterprise-risk-dr-analytics/
├── dashboard/
├── data/
├── database/
├── docs/
├── notebooks/
├── reports/
├── sql/
├── src/
├── tests/
├── requirements.txt
└── README.md
```

## Project Purpose

This portfolio project demonstrates practical skills in:

- IT Risk Management
- Disaster Recovery and Business Continuity
- Data Analytics
- SQL and Python
- Data Validation
- Business Intelligence
- Risk-Based Management Reporting
