-- QUERY 1: Get the latest risk assessment for every application

WITH Ranked_Risks AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY Application_ID
            ORDER BY Assessment_Date DESC
        ) AS Risk_Rank
    FROM risk_assessments
)

SELECT
    Application_ID,
    Assessment_Date,
    Inherent_Risk_Score,
    Control_Effectiveness_Percent,
    Residual_Risk_Score,
    Risk_Level
FROM Ranked_Risks
WHERE Risk_Rank = 1
ORDER BY Residual_Risk_Score DESC;

-- QUERY 2: Latest risk profile of every application

WITH Ranked_Risks AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY Application_ID
            ORDER BY Assessment_Date DESC
        ) AS Risk_Rank
    FROM risk_assessments
)

SELECT
    a.Application_ID,
    a.Application_Name,
    b.Business_Unit_Name,
    a.Criticality,
    r.Assessment_Date,
    r.Inherent_Risk_Score,
    r.Control_Effectiveness_Percent,
    r.Residual_Risk_Score,
    r.Risk_Level
FROM applications a

INNER JOIN business_units b
    ON a.Business_Unit_ID = b.Business_Unit_ID

LEFT JOIN Ranked_Risks r
    ON a.Application_ID = r.Application_ID
    AND r.Risk_Rank = 1

ORDER BY r.Residual_Risk_Score DESC;

-- QUERY 3: Identify risk score trends

WITH Risk_Trends AS (
    SELECT
        Application_ID,
        Assessment_Date,
        Residual_Risk_Score,

        LAG(Residual_Risk_Score) OVER (
            PARTITION BY Application_ID
            ORDER BY Assessment_Date
        ) AS Previous_Risk_Score

    FROM risk_assessments
),

Latest_Trends AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY Application_ID
            ORDER BY Assessment_Date DESC
        ) AS Risk_Rank
    FROM Risk_Trends
)

SELECT
    Application_ID,
    Assessment_Date,
    Previous_Risk_Score,
    Residual_Risk_Score AS Latest_Risk_Score,

    Residual_Risk_Score - Previous_Risk_Score
        AS Risk_Score_Change,

    CASE
        WHEN Residual_Risk_Score > Previous_Risk_Score
            THEN 'Risk Increased'
        WHEN Residual_Risk_Score < Previous_Risk_Score
            THEN 'Risk Decreased'
        ELSE 'No Change'
    END AS Risk_Trend

FROM Latest_Trends
WHERE Risk_Rank = 1
ORDER BY Risk_Score_Change DESC;

-- QUERY 4: High and Critical risk applications

WITH Ranked_Risks AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY Application_ID
            ORDER BY Assessment_Date DESC
        ) AS Risk_Rank
    FROM risk_assessments
)

SELECT
    a.Application_ID,
    a.Application_Name,
    b.Business_Unit_Name,
    a.Criticality,
    r.Residual_Risk_Score,
    r.Risk_Level

FROM applications a

INNER JOIN business_units b
    ON a.Business_Unit_ID = b.Business_Unit_ID

INNER JOIN Ranked_Risks r
    ON a.Application_ID = r.Application_ID

WHERE r.Risk_Rank = 1
AND r.Risk_Level IN ('High', 'Critical')

ORDER BY r.Residual_Risk_Score DESC;


PRAGMA table_info(dr_assessments);

-- QUERY 6: Combined Enterprise Risk and DR Readiness Analysis

WITH Ranked_Risks AS (

    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY Application_ID
            ORDER BY Assessment_Date DESC
        ) AS Risk_Rank

    FROM risk_assessments
),

DR_Summary AS (

    SELECT
        Application_ID,

        COUNT(*) AS Total_DR_Tests,

        SUM(
            CASE WHEN DR_Test_Result = 'Failed'
            THEN 1 ELSE 0 END
        ) AS Failed_DR_Tests,

        SUM(
            CASE WHEN RTO_Status = 'Breached'
            THEN 1 ELSE 0 END
        ) AS RTO_Breaches,

        SUM(
            CASE WHEN RPO_Status = 'Breached'
            THEN 1 ELSE 0 END
        ) AS RPO_Breaches,

        ROUND(
            AVG(Actual_Recovery_Time_Hours), 2
        ) AS Average_Recovery_Time,

        ROUND(
            AVG(Actual_Data_Loss_Hours), 2
        ) AS Average_Data_Loss

    FROM dr_assessments
    GROUP BY Application_ID
)

SELECT

    a.Application_ID,
    a.Application_Name,
    b.Business_Unit_Name,
    a.Criticality,

    r.Residual_Risk_Score,
    r.Risk_Level,

    d.Total_DR_Tests,
    d.Failed_DR_Tests,
    d.RTO_Breaches,
    d.RPO_Breaches,

    d.Average_Recovery_Time,
    d.Average_Data_Loss,

    CASE
        WHEN r.Risk_Level IN ('High', 'Critical')
             AND d.Failed_DR_Tests > 0
             AND a.Criticality IN ('High', 'Critical')
            THEN 'Immediate Attention'

        WHEN d.RTO_Breaches > 0 OR d.RPO_Breaches > 0
            THEN 'DR Remediation Required'

        WHEN r.Risk_Level IN ('High', 'Critical')
            THEN 'Risk Remediation Required'

        ELSE 'Normal Monitoring'
    END AS Management_Priority

FROM applications a

INNER JOIN business_units b
    ON a.Business_Unit_ID = b.Business_Unit_ID

LEFT JOIN Ranked_Risks r
    ON a.Application_ID = r.Application_ID
    AND r.Risk_Rank = 1

LEFT JOIN DR_Summary d
    ON a.Application_ID = d.Application_ID

ORDER BY
    CASE Management_Priority
        WHEN 'Immediate Attention' THEN 1
        WHEN 'DR Remediation Required' THEN 2
        WHEN 'Risk Remediation Required' THEN 3
        ELSE 4
    END,
    r.Residual_Risk_Score DESC;