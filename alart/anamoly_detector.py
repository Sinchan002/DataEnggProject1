# alerts/anomaly_detector.py
import pandas as pd
import numpy as np
import smtplib
from email.mime.text import MIMEText

SPIKE_THRESHOLD_STD = 3.0  # flag if > 3 standard deviations above mean

def detect_commission_spikes(df: pd.DataFrame) -> pd.DataFrame:
    """Z-score based spike detection per broker."""
    stats = df.groupby("broker_id")["commission_earned"].agg(["mean", "std"]).reset_index()
    df = df.merge(stats, on="broker_id")
    df["z_score"] = (df["commission_earned"] - df["mean"]) / df["std"].replace(0, np.nan)
    return df[df["z_score"].abs() > SPIKE_THRESHOLD_STD]

def detect_with_iqr(df: pd.DataFrame) -> pd.DataFrame:
    """IQR-based outlier detection — robust to non-normal distributions."""
    q1 = df["commission_earned"].quantile(0.25)
    q3 = df["commission_earned"].quantile(0.75)
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return df[(df["commission_earned"] < lower) | (df["commission_earned"] > upper)]

def send_alert(anomalies: pd.DataFrame, to: str = "alerts@company.com"):
    if anomalies.empty:
        print("No anomalies detected.")
        return
    body = f"Commission spike detected in {len(anomalies)} trade(s):\n\n"
    body += anomalies[["trade_id", "broker_id", "commission_earned", "z_score"]
                       ].to_string(index=False)
    msg = MIMEText(body)
    msg["Subject"] = f"[ALERT] Broker Commission Spike — {len(anomalies)} anomalies"
    msg["From"]    = "pipeline@company.com"
    msg["To"]      = to
    # with smtplib.SMTP("smtp.company.com") as s:
    #     s.send_message(msg)
    print("ALERT SENT:\n", body)  # replace with real SMTP in prod

def run():
    df = pd.read_parquet("data/processed/fact_commissions.parquet")
    spikes = detect_commission_spikes(df)
    send_alert(spikes)