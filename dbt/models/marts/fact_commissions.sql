-- dbt/models/marts/fact_commissions.sql
{{ config(materialized='incremental', unique_key='trade_id') }}

WITH transactions AS (
    SELECT * FROM {{ ref('stg_transactions') }}
    WHERE status = 'completed'
),

brokers AS (
    SELECT * FROM {{ ref('stg_brokers') }}
)

SELECT
    t.trade_id,
    t.broker_id,
    t.client_id,
    t.date::DATE                                       AS date_id,
    t.transaction_amount,
    b.commission_rate,
    ROUND(t.transaction_amount * b.commission_rate, 2) AS commission_earned,
    t.product_type,
    b.region,
    CURRENT_TIMESTAMP                                  AS dbt_updated_at

FROM transactions t
LEFT JOIN brokers b USING (broker_id)

{% if is_incremental() %}
WHERE t.date > (SELECT MAX(date_id) FROM {{ this }})
{% endif %}