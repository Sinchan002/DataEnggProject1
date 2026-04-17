-- sql/create_tables.sql

-- Dimension: Brokers
CREATE TABLE dim_broker (
    broker_id       VARCHAR(10)    PRIMARY KEY,
    name            VARCHAR(100)   NOT NULL,
    region          VARCHAR(50),
    commission_rate DECIMAL(6, 4)  NOT NULL,
    effective_from  DATE           DEFAULT CURRENT_DATE,
    is_active       BOOLEAN        DEFAULT TRUE
);

-- Dimension: Clients
CREATE TABLE dim_client (
    client_id   VARCHAR(10)  PRIMARY KEY,
    client_name VARCHAR(100),
    segment     VARCHAR(50)  -- Retail, Institutional, HNI
);

-- Dimension: Time (pre-populated)
CREATE TABLE dim_date (
    date_id       DATE PRIMARY KEY,
    day_of_week   SMALLINT,
    week_number   SMALLINT,
    month         SMALLINT,
    quarter       SMALLINT,
    year          SMALLINT,
    is_weekend    BOOLEAN
);

-- Fact: Transactions + computed commission
CREATE TABLE fact_commission (
    trade_id            VARCHAR(20)    PRIMARY KEY,
    broker_id           VARCHAR(10)    REFERENCES dim_broker(broker_id),
    client_id           VARCHAR(10)    REFERENCES dim_client(client_id),
    date_id             DATE           REFERENCES dim_date(date_id),
    transaction_amount  DECIMAL(18, 2) NOT NULL,
    commission_rate     DECIMAL(6, 4)  NOT NULL,
    commission_earned   DECIMAL(18, 2) GENERATED ALWAYS AS
                            (transaction_amount * commission_rate) STORED,
    product_type        VARCHAR(50),
    status              VARCHAR(20),
    ingested_at         TIMESTAMP      DEFAULT NOW()
);

-- Aggregate: broker daily summary (materialized for dashboard)
CREATE TABLE agg_broker_daily (
    broker_id             VARCHAR(10),
    date_id               DATE,
    total_transactions    INTEGER,
    total_trade_volume    DECIMAL(18, 2),
    total_commission      DECIMAL(18, 2),
    avg_commission        DECIMAL(18, 2),
    PRIMARY KEY (broker_id, date_id)
);