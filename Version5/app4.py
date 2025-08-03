import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Multi-Company Stock Dashboard", layout="wide")

st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to:", ["📊 Stock Dashboard", "👥 Visitor Logs"])

# --- Page: Stock Dashboard ---
if page == "📊 Stock Dashboard":
    st.title("📊 Multi-Company Stock Dashboard")

    uploaded_files = st.file_uploader("Upload CSV files for companies", type="csv", accept_multiple_files=True)

    if uploaded_files:
        for file in uploaded_files:
            company_name = file.name.replace(".csv", "")
            df = pd.read_csv(file, parse_dates=["Date"])

            st.subheader(f"📈 {company_name} Stock Overview")

            # Basic stats
            st.write("🔹 Latest Close Price:", df["Close"].iloc[-1])
            st.write("🔹 Average Volume:", round(df["Volume"].mean(), 2))

            # Moving Average
            df["MA_20"] = df["Close"].rolling(window=20).mean()

            # Plot
            fig = px.line(df, x="Date", y=["Close", "MA_20"],
                          labels={"value": "Price", "variable": "Metric"},
                          title=f"{company_name} - Close Price & MA(20)")
            st.plotly_chart(fig, use_container_width=True)

            # Volume Bar Chart
            vol_fig = px.bar(df, x="Date", y="Volume", title=f"{company_name} - Volume")
            st.plotly_chart(vol_fig, use_container_width=True)
    else:
        st.info("📂 Upload one or more CSV files to begin.")

# --- Page: Visitor Logs ---
elif page == "👥 Visitor Logs":
    st.title("👥 Visitor Logs")
    logs = pd.read_csv("user_logs.csv")
    st.dataframe(logs)
