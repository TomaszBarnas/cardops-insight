import streamlit as st
import pandas as pd

from modules.analyzer import analyze_transactions
from modules.anomaly_detector import detect_anomalies
from modules.errors import DataValidationError

REQUIRED_COLUMNS = {
    'transaction_id',
    'card_number',
    'amount',
    'currency',
    'timestamp',
    'status'
}

st.set_page_config(page_title="CardOps Insight", layout="wide")
st.title("📊 CardOps Insight – Transaction Dashboard")

uploaded_file = st.file_uploader("Upload transaction CSV file", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

        missing_cols = REQUIRED_COLUMNS - set(df.columns)
        if missing_cols:
            raise DataValidationError(f"Missing columns: {', '.join(missing_cols)}")

    except DataValidationError as e:
        st.error(f"❌ Validation error: {e}")
        st.stop()
    except Exception as e:
        st.error(f"❌ Failed to process file: {e}")
        st.stop()

    st.success("File loaded successfully.")
    st.write("Preview of data:", df.head())

    with st.expander("🔍 Summary Statistics", expanded=True):
        summary = analyze_transactions(df)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Transactions", summary["total_transactions"])
        col2.metric("Total Amount", f"{summary['total_amount']:.2f}")
        col3.metric("Average Amount", f"{summary['average_amount']:.2f}")

        st.subheader("Transactions by Status")
        st.bar_chart(pd.Series(summary["transactions_by_status"]))

        st.subheader("Transactions per Day")
        st.line_chart(pd.Series(summary["transactions_per_day"]))

        st.subheader("Top Active Cards")
        st.table(pd.Series(summary["top_active_cards"]).to_frame("Count"))

    with st.expander("⚠️ Anomalies"):
        anomalies = detect_anomalies(df)

        if not anomalies.empty:
            st.warning(f"{len(anomalies)} anomalies detected.")
            st.dataframe(anomalies)
        else:
            st.success("No anomalies detected.")
else:
    st.info("Please upload a CSV file to begin.")
