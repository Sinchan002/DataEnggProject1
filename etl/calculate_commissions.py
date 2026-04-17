# etl/calculate_commissions.py
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_raw(tx_path: str, broker_path: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    tx = pd.read_csv(tx_path, parse_dates=["date"])
    br = pd.read_csv(broker_path)
    return tx, br

def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df[df["status"] == "completed"].copy()  # only settled trades
    df = df.dropna(subset=["broker_id", "client_id", "transaction_amount"])
    df = df.drop_duplicates(subset=["trade_id"])
    df["transaction_amount"] = pd.to_numeric(df["transaction_amount"], errors="coerce")
    df = df[df["transaction_amount"] > 0]
    logger.info(f"Cleaned: {before} → {len(df)} rows retained")
    return df

def calculate_commissions(tx: pd.DataFrame, brokers: pd.DataFrame) -> pd.DataFrame:
    df = tx.merge(
        brokers[["broker_id", "name", "region", "commission_rate"]],
        on="broker_id", how="left"
    )
    df["commission_earned"] = (
        df["transaction_amount"] * df["commission_rate"]
    ).round(2)
    return df

def aggregate_by_broker(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["broker_id", "name", "region"])
          .agg(
              total_trades=("trade_id", "count"),
              total_volume=("transaction_amount", "sum"),
              total_commission=("commission_earned", "sum"),
              avg_commission=("commission_earned", "mean"),
          )
          .reset_index()
          .sort_values("total_commission", ascending=False)
    )

def aggregate_daily(df: pd.DataFrame) -> pd.DataFrame:
    df["date"] = pd.to_datetime(df["date"]).dt.date
    return (
        df.groupby(["date", "broker_id"])
          .agg(total_commission=("commission_earned", "sum"))
          .reset_index()
    )

if __name__ == "__main__":
    tx, brokers = load_raw(
        "data/sample/transactions.csv",
        "data/sample/brokers.csv"
    )
    tx_clean   = clean_transactions(tx)
    enriched   = calculate_commissions(tx_clean, brokers)
    by_broker  = aggregate_by_broker(enriched)
    daily      = aggregate_daily(enriched)

    enriched.to_parquet("data/processed/fact_commissions.parquet", index=False)
    by_broker.to_csv("data/processed/agg_broker.csv", index=False)
    daily.to_csv("data/processed/agg_daily.csv", index=False)
    print(by_broker.head(10).to_string(index=False))