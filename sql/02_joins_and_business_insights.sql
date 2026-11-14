-- QUERY 1: Applications with their Business Units

SELECT
    a.Application_ID,
    a.Application_Name,
    a.Criticality,
    b.Business_Unit_Name,
    b.Location
FROM applications a
INNER JOIN business_units b
    ON a.Business_Unit_ID = b.Business_Unit_ID;

-- QUERY 2: Average residual risk by Business Unit

SELECT
    b.Business_Unit_Name,
    COUNT(DISTINCT a.Application_ID) AS Total_Applications,
    ROUND(AVG(r.Residual_Risk_Score), 2) AS Average_Residual_Risk
FROM applications a
INNER JOIN business_units b
    ON a.Business_Unit_ID = b.Business_Unit_ID
INNER JOIN risk_assessments r
    ON a.Application_ID = r.Application_ID
GROUP BY b.Business_Unit_Name
ORDER BY Average_Residual_Risk DESC; 

-- QUERY 3: DR testing performance by Application

SELECT
    a.Application_ID,
    a.Application_Name,
    a.Criticality,
    COUNT(d.Application_ID) AS Total_DR_Tests,
    SUM(
        CASE
            WHEN d.DR_Test_Result = 'Failed' THEN 1
            ELSE 0
        END
    ) AS Failed_DR_Tests,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN d.DR_Test_Result = 'Passed' THEN 1
                ELSE 0
            END
        ) / COUNT(d.Application_ID),
        2
    ) AS DR_Pass_Rate
FROM applications a
LEFT JOIN dr_assessments d
    ON a.Application_ID = d.Application_ID
GROUP BY
    a.Application_ID,
    a.Application_Name,
    a.Criticality
ORDER BY Failed_DR_Tests DESC;

-- QUERY 4: Incident exposure by Business Unit

SELECT
    b.Business_Unit_Name,
    COUNT(i.Incident_ID) AS Total_Incidents,
    ROUND(SUM(i.Financial_Impact_INR), 2) AS Total_Financial_Impact_INR,
    ROUND(AVG(i.Downtime_Hours), 2) AS Average_Downtime_Hours
FROM applications a
INNER JOIN business_units b
    ON a.Business_Unit_ID = b.Business_Unit_ID
LEFT JOIN incidents i
    ON a.Application_ID = i.Application_ID
GROUP BY b.Business_Unit_Name
ORDER BY Total_Financial_Impact_INR DESC;