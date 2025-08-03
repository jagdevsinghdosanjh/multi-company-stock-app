# app.py

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import datetime
import os
import requests
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# --- Configuration ---
LOG_FILE = "user_logs.csv"
API_KEY = os.environ.get("POLYGON_API_KEY")
BASE_URL = "https://api.polygon.io/v2/aggs/ticker"
START_DATE = "2025-01-01"
END_DATE = "2025-05-11"

# --- Company Tickers ---
COMPANIES = {
    "Apple Inc. (AAPL)": "AAPL",
    "Alphabet Inc. (GOOGL)": "GOOGL",
    "Microsoft Corporation (MSFT)": "MSFT",
    "NVIDIA Corporation (NVDA)": "NVDA",
    "Tesla, Inc. (TSLA)": "TSLA",
    "Infosys Ltd. (INFY)": "INFY",
    "Amazon.com, Inc. (AMZN)": "AMZN",
    "Meta Platforms, Inc. (META)": "META",
    "Intel Corporation (INTC)": "INTC",
    "Advanced Micro Devices, Inc. (AMD)": "AMD"
}

# --- Visitor Logging ---
if not os.path.exists(LOG_FILE):
    pd.DataFrame(columns=["Timestamp", "Device", "Latitude", "Longitude"]).to_csv(LOG_FILE, index=False)

# Inject JavaScript to collect device and location info
components.html("""
    <script src="logger.js"></script>
""", height=0)

params = st.query_params
if "device" in params and "latitude" in params and "longitude" in params:
    device = params["device"]
    lat = params["latitude"]
    lon = params["longitude"]
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if "logged" not in st.session_state:
        pd.DataFrame([[timestamp, device, lat, lon]],
                     columns=["Timestamp", "Device", "Latitude", "Longitude"]).to_csv(LOG_FILE, mode='a', header=False, index=False)
        st.session_state.logged = True

# --- Authenticator Setup ---
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login("Login", "sidebar")

if authentication_status is False:
    st.error("❌ Incorrect username or password")
elif authentication_status is None:
    st.warning("🔐 Please log in to continue")
elif authentication_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.success(f"✅ Logged in as {name}")

    # --- Sidebar Navigation ---
    st.sidebar.title("📌 Navigation")
    page = st.sidebar.radio("Go to:", ["📊 Stock Dashboard", "👥 Visitor Logs"])

    # --- Page: Stock Dashboard ---
    if page == "📊 Stock Dashboard":
        st.title("📊 Multi-Company Stock Dashboard")

        selected_company = st.selectbox("Select a Company", list(COMPANIES.keys()))
        ticker = COMPANIES[selected_company]

        def fetch_stock_data(ticker):
            if not API_KEY:
                st.error("API key not found. Please set POLYGON_API_KEY in your environment.")
                return None

            url = f"{BASE_URL}/{ticker}/range/1/day/{START_DATE}/{END_DATE}?apiKey={API_KEY}"
            response = requests.get(url)
            if response.status_code != 200:
                st.error("Failed to fetch data.")
                return None
            data = response.json()
            if "results" not in data:
                st.warning("No results found.")
                return None
            df = pd.DataFrame(data["results"])
            df["date"] = pd.to_datetime(df["t"], unit="ms").dt.date
            df = df.rename(columns={
                "v": "Volume",
                "vw": "VWAP",
                "o": "Open",
                "c": "Close",
                "h": "High",
                "l": "Low",
                "n": "Trades"
            })
            return df[["date", "Volume", "VWAP", "Open", "Close", "High", "Low", "Trades"]]

        df = fetch_stock_data(ticker)

        if df is not None:
            st.subheader(f"📈 {selected_company} Stock Data")
            st.dataframe(df, use_container_width=True)

            st.line_chart(df.set_index("date")[["Open", "Close", "High", "Low"]])
            st.bar_chart(df.set_index("date")["Volume"])
        else:
            st.stop()

    # --- Page: Visitor Logs ---
    elif page == "👥 Visitor Logs":
        st.title("👥 Visitor Logs")
        logs = pd.read_csv(LOG_FILE)
        st.dataframe(logs)
