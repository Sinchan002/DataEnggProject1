# analytics/dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Broker Commission Tracker", layout="wide")
st.title("Broker Commission Tracker")

@st.cache_data
def load_data():
    enriched = pd.read_parquet("data/processed/fact_commissions.parquet")
    by_broker = pd.read_csv("data/processed/agg_broker.csv")
    daily     = pd.read_csv("data/processed/agg_daily.csv", parse_dates=["date"])
    return enriched, by_broker, daily

enriched, by_broker, daily = load_data()

# --- KPI row ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Commissions", f"${enriched['commission_earned'].sum():,.0f}")
col2.metric("Total Trades",       f"{len(enriched):,}")
col3.metric("Active Brokers",     by_broker["broker_id"].nunique())
col4.metric("Avg Commission",     f"${enriched['commission_earned'].mean():,.2f}")

st.divider()

# --- Top brokers bar chart ---
st.subheader("Top brokers by commission earned")
fig1 = px.bar(
    by_broker.head(10),
    x="name", y="total_commission",
    color="region",
    labels={"total_commission": "Commission ($)", "name": "Broker"},
    color_discrete_sequence=px.colors.qualitative.Pastel,
)
st.plotly_chart(fig1, use_container_width=True)

# --- Region pie ---
col_a, col_b = st.columns(2)
with col_a:
    st.subheader("Region-wise commission split")
    region_df = by_broker.groupby("region")["total_commission"].sum().reset_index()
    fig2 = px.pie(region_df, names="region", values="total_commission")
    st.plotly_chart(fig2, use_container_width=True)

# --- Daily trend ---
with col_b:
    st.subheader("Daily commission trend")
    daily_agg = daily.groupby("date")["total_commission"].sum().reset_index()
    fig3 = px.line(daily_agg, x="date", y="total_commission",
                   labels={"total_commission": "Commission ($)"})
    st.plotly_chart(fig3, use_container_width=True)

# --- Anomaly table ---
st.subheader("Flagged anomalies (Z-score > 3)")
enriched["z_score"] = (
    enriched["commission_earned"] - enriched["commission_earned"].mean()
) / enriched["commission_earned"].std()
anomalies = enriched[enriched["z_score"].abs() > 3]
st.dataframe(
    anomalies[["trade_id", "broker_id", "commission_earned", "z_score"]],
    use_container_width=True
)