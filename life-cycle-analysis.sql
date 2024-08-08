WITH transaction_data AS (
    SELECT
        CustomerID,
        InvoiceDate,
        LAG(InvoiceDate) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate) AS previous_date
    FROM `test-data-431401.transaction.data-trans`
),
churn_data AS (
    SELECT
        CustomerID,
        InvoiceDate,
        previous_date,
        IFNULL(DATE_DIFF(InvoiceDate, previous_date, DAY), 0) AS days_since_last_purchase,
        CASE 
            WHEN IFNULL(DATE_DIFF(InvoiceDate, previous_date, DAY), 0) > 10 THEN 1 
            ELSE 0 
        END AS churn_flag
    FROM transaction_data
),
cycle_sequence_data AS (
    SELECT
        CustomerID,
        InvoiceDate,
        previous_date,
        days_since_last_purchase,
        churn_flag,
        SUM(churn_flag) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate) + 1 AS lifetime_cycle_sequence,
        ROW_NUMBER() OVER (PARTITION BY CustomerID ORDER BY InvoiceDate) AS purchase_sequence
    FROM churn_data
)
SELECT
    t.*,
    csd.lifetime_cycle_sequence,
    csd.purchase_sequence
FROM `test-data-431401.transaction.data-trans` t
JOIN cycle_sequence_data csd
ON t.CustomerID = csd.CustomerID AND t.InvoiceDate = csd.InvoiceDate
ORDER BY t.CustomerID, t.InvoiceDate;
