import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import datetime
import os

LOG_FILE = "user_logs.csv"

# Initialize log file if not exists
if not os.path.exists(LOG_FILE):
    df = pd.DataFrame(columns=["Timestamp", "Device", "Latitude", "Longitude"])
    df.to_csv(LOG_FILE, index=False)

# Inject JavaScript to collect device and location info
components.html("""
    <script>
        async function logUserInfo() {
            const device = navigator.userAgent;
            let lat = "N/A", lon = "N/A";

            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(position) {
                    lat = position.coords.latitude;
                    lon = position.coords.longitude;

                    const form = document.createElement('form');
                    form.method = 'POST';
                    form.action = '';
                    form.style.display = 'none';

                    const deviceInput = document.createElement('input');
                    deviceInput.name = 'device';
                    deviceInput.value = device;
                    form.appendChild(deviceInput);

                    const latInput = document.createElement('input');
                    latInput.name = 'latitude';
                    latInput.value = lat;
                    form.appendChild(latInput);

                    const lonInput = document.createElement('input');
                    lonInput.name = 'longitude';
                    lonInput.value = lon;
                    form.appendChild(lonInput);

                    document.body.appendChild(form);
                    form.submit();
                });
            }
        }
        logUserInfo();
    </script>
""", height=0)

# Handle form submission
if st.experimental_get_query_params():
    pass  # Prevent rerun loop

if st.request.method == "POST":
    device = st.request.form.get("device", "Unknown")
    lat = st.request.form.get("latitude", "N/A")
    lon = st.request.form.get("longitude", "N/A")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Append to CSV
    new_log = pd.DataFrame([[timestamp, device, lat, lon]],
                           columns=["Timestamp", "Device", "Latitude", "Longitude"])
    new_log.to_csv(LOG_FILE, mode='a', header=False, index=False)

# Display logs
st.markdown("### 👥 Visitor Logs")
logs = pd.read_csv(LOG_FILE)
st.dataframe(logs)

# import streamlit as st
# import requests
# import pandas as pd
# import os
# from datetime import datetime  # ✅ Now meaningfully used
# import streamlit as st

# # Header
# st.markdown("""
#     <div style='background-color:#0E1117; padding:15px; border-radius:10px;'>
#         <h1 style='color:#F5F5F5; text-align:center;'>📊 Stock Explorer Dashboard</h1>
#         <p style='color:#CCCCCC; text-align:center;'>Track real-time data for top global and Indian companies</p>
#     </div>
#     <br>
# """, unsafe_allow_html=True)


# # --- Configuration ---
# BASE_URL = "https://api.polygon.io/v2/aggs/ticker"
# API_KEY = os.environ.get("POLYGON_API_KEY")
# START_DATE = "2025-01-01"
# END_DATE = "2025-07-31"

# # --- Company Options ---
# COMPANIES = {
#     "Apple Inc. (AAPL)": "AAPL",
#     "Alphabet Inc. (GOOGL)": "GOOGL",
#     "Microsoft Corporation (MSFT)": "MSFT",
#     "NVIDIA Corporation (NVDA)": "NVDA",
#     "Tesla, Inc. (TSLA)": "TSLA",
#     "Infosys Ltd. (INFY)": "INFY",
#     "Amazon.com, Inc. (AMZN)": "AMZN",
#     "Meta Platforms, Inc. (META)": "META",
#     "Intel Corporation (INTC)": "INTC",
#     "Advanced Micro Devices, Inc. (AMD)": "AMD",
#     "Oracle Corporation (ORCL)": "ORCL",
#     "Cisco Systems, Inc. (CSCO)": "CSCO",
#     "IBM Corporation (IBM)": "IBM",
#     "Reliance Industries Ltd. (RELIANCE)": "RELIANCE",
#     "Tata Consultancy Services Ltd. (TCS)": "TCS",
#     "HCL Technologies Ltd. (HCLTECH)": "HCLTECH",
#     "Wipro Ltd. (WIPRO)": "WIPRO",
#     "Bharti Airtel Ltd. (BHARTIARTL)": "BHARTIARTL",
#     "ICICI Bank Ltd. (ICICIBANK)": "ICICIBANK",
#     "HDFC Bank Ltd. (HDFCBANK)": "HDFCBANK"
# }


# # --- Streamlit UI ---
# st.set_page_config(page_title="Multi-Company Stock App", layout="wide")
# st.title("📈 Multi-Company Stock Data Viewer")

# # ✅ Display current date using datetime
# st.caption(f"📅 Today's Date: {datetime.now().strftime('%A, %d %B %Y')}")

# selected_company = st.selectbox("Select a Company", list(COMPANIES.keys()))
# ticker = COMPANIES[selected_company]

# # --- Fetch Data ---
# @st.cache_data(ttl=3600)
# def fetch_stock_data(ticker):
#     if not API_KEY:
#         st.error("API key not found. Please set POLYGON_API_KEY in your environment.")
#         return None

#     url = f"{BASE_URL}/{ticker}/range/1/day/{START_DATE}/{END_DATE}?apiKey={API_KEY}"
#     response = requests.get(url)
#     if response.status_code != 200:
#         st.error("Failed to fetch data.")
#         return None
#     data = response.json()
#     if "results" not in data:
#         st.warning("No results found.")
#         return None
#     df = pd.DataFrame(data["results"])
#     df["date"] = pd.to_datetime(df["t"], unit="ms").dt.date
#     df = df.rename(columns={
#         "v": "Volume",
#         "vw": "VWAP",
#         "o": "Open",
#         "c": "Close",
#         "h": "High",
#         "l": "Low",
#         "n": "Trades"
#     })
#     return df[["date", "Volume", "VWAP", "Open", "Close", "High", "Low", "Trades"]]

# df = fetch_stock_data(ticker)

# # --- Display Data ---
# if df is not None:
#     st.subheader(f"Stock Data for {selected_company}")
#     st.dataframe(df, use_container_width=True)

#     # --- Chart ---
#     st.subheader("📊 Price Trend")
#     st.line_chart(df.set_index("date")[["Open", "Close", "High", "Low"]])
# else:
#     st.stop()
# # Footer
# st.markdown("""
#     <br><hr>
#     <div style='text-align:center; color:#888888; font-size:14px;'>
#         Made with ❤️ by Jagdev Singh Dosanjh<br>
#         Powered by Polygon.io & Streamlit<br>
#         <a href="https://dosanjhpubsasr.org">DOSANJHPUBSASR.ORG</a>
#     </div>
# """, unsafe_allow_html=True)
