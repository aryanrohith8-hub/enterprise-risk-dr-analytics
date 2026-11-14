-- QUERY 1: Enterprise Risk and DR Management KPIs

WITH Ranked_Risks AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY Application_ID
            ORDER BY Assessment_Date DESC
        ) AS Risk_Rank
    FROM risk_assessments
),

Latest_Risks AS (
    SELECT *
    FROM Ranked_Risks
    WHERE Risk_Rank = 1
),

DR_KPIs AS (
    SELECT
        COUNT(*) AS Total_DR_Tests,

        SUM(
            CASE WHEN DR_Test_Result = 'Passed'
            THEN 1 ELSE 0 END
        ) AS Passed_DR_Tests,

        SUM(
            CASE WHEN RTO_Status = 'Breached'
            THEN 1 ELSE 0 END
        ) AS Total_RTO_Breaches,

        SUM(
            CASE WHEN RPO_Status = 'Breached'
            THEN 1 ELSE 0 END
        ) AS Total_RPO_Breaches

    FROM dr_assessments
)

SELECT

    (SELECT COUNT(*)
     FROM applications) AS Total_Applications,

    (SELECT COUNT(*)
     FROM applications
     WHERE Criticality IN ('Critical', 'High')
    ) AS High_Criticality_Applications,

    (SELECT ROUND(AVG(Residual_Risk_Score), 2)
     FROM Latest_Risks
    ) AS Average_Residual_Risk,

    d.Total_DR_Tests,

    d.Passed_DR_Tests,

    ROUND(
        100.0 * d.Passed_DR_Tests /
        NULLIF(d.Total_DR_Tests, 0),
        2
    ) AS DR_Pass_Percentage,

    d.Total_RTO_Breaches,

    d.Total_RPO_Breaches

FROM DR_KPIs d;

-- QUERY 2: Risk Exposure by Business Unit

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
    b.Business_Unit_Name,

    COUNT(a.Application_ID) AS Total_Applications,

    ROUND(
        AVG(r.Residual_Risk_Score), 2
    ) AS Average_Residual_Risk,

    SUM(
        CASE WHEN r.Risk_Level IN ('High', 'Critical')
        THEN 1 ELSE 0 END
    ) AS High_Risk_Applications

FROM applications a

INNER JOIN business_units b
    ON a.Business_Unit_ID = b.Business_Unit_ID

LEFT JOIN Ranked_Risks r
    ON a.Application_ID = r.Application_ID
    AND r.Risk_Rank = 1

GROUP BY b.Business_Unit_Name

ORDER BY Average_Residual_Risk DESC;

-- QUERY 3: Applications by Management Priority

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
        ) AS RPO_Breaches

    FROM dr_assessments
    GROUP BY Application_ID
),

Application_Priorities AS (
    SELECT
        a.Application_ID,

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

    LEFT JOIN Ranked_Risks r
        ON a.Application_ID = r.Application_ID
        AND r.Risk_Rank = 1

    LEFT JOIN DR_Summary d
        ON a.Application_ID = d.Application_ID
)

SELECT
    Management_Priority,
    COUNT(*) AS Application_Count

FROM Application_Priorities

GROUP BY Management_Priority

ORDER BY Application_Count DESC;