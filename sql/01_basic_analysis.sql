
-- 1. Display all Critical applications

SELECT *
FROM applications
WHERE Criticality = 'Critical';


-- 2. Find the 10 applications with the
-- strictest RTO requirements

SELECT
    Application_Name,
    Criticality,
    Target_RTO_Hours
FROM applications
ORDER BY Target_RTO_Hours ASC
LIMIT 10;


-- 3. Count applications by criticality

SELECT
    Criticality,
    COUNT(*) AS Total_Applications
FROM applications
GROUP BY Criticality;


-- 4. Calculate average residual risk

SELECT
    ROUND(AVG(Residual_Risk_Score), 2)
    AS Average_Residual_Risk
FROM risk_assessments;


-- 5. Calculate total financial impact
-- by incident severity

SELECT
    Severity,
    ROUND(SUM(Financial_Impact_INR), 2)
    AS Total_Financial_Impact
FROM incidents
GROUP BY Severity
ORDER BY Total_Financial_Impact DESC;
