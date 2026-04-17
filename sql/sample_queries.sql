-- sql/sample_queries.sql

-- Top 10 brokers by total commission this month
SELECT
    b.name,
    b.region,
    SUM(f.commission_earned)   AS total_commission,
    COUNT(f.trade_id)          AS total_trades,
    AVG(f.commission_earned)   AS avg_per_trade
FROM fact_commission f
JOIN dim_broker b USING (broker_id)
WHERE DATE_TRUNC('month', f.date_id) = DATE_TRUNC('month', CURRENT_DATE)
GROUP BY b.name, b.region
ORDER BY total_commission DESC
LIMIT 10;

-- Monthly commission trend per region
SELECT
    TO_CHAR(date_id, 'YYYY-MM') AS month,
    region,
    SUM(commission_earned)      AS total_commission
FROM fact_commission f
JOIN dim_broker b USING (broker_id)
GROUP BY month, region
ORDER BY month, region;

-- Detect spikes: commissions > broker's 30-day average × 2
WITH broker_avg AS (
    SELECT broker_id, AVG(commission_earned) AS avg_30d
    FROM fact_commission
    WHERE date_id >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY broker_id
)
SELECT f.trade_id, f.broker_id, f.commission_earned,
       a.avg_30d, f.commission_earned / a.avg_30d AS spike_ratio
FROM fact_commission f
JOIN broker_avg a USING (broker_id)
WHERE f.commission_earned > a.avg_30d * 2
ORDER BY spike_ratio DESC;