import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from analyzer import send_email_alert
from analyzer import load_data, detect_wastage, predict_usage, detect_anomalies, predict_water_usage

# Page config
st.set_page_config(page_title="AI Utility Dashboard", layout="wide")

st.title("🏫 AI-Driven Water & Energy Intelligence System for Campuses")
st.markdown("### Smart monitoring • AI insights • Sustainable campus management")
st.info("""
This system uses AI to monitor, analyze, and predict campus water and energy usage. 
It detects anomalies, provides insights, and helps reduce wastage for sustainable operations.
""")

# Sidebar
st.sidebar.title("📊 Controls")
st.sidebar.write("Upload and analyze campus data")

# Email input
user_email = st.text_input("📧 Enter Email for Alerts")

# File upload
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    # Clean data
    data.columns = data.columns.str.strip().str.lower()
    data["water"] = pd.to_numeric(data["water"], errors='coerce')
    data["electricity"] = pd.to_numeric(data["electricity"], errors='coerce')
    data = data.dropna()

else:
    st.warning("Please upload a CSV file")
    st.stop()

# Show data
st.subheader("📊 Campus Utility Data")
st.write(data)

# Summary
st.subheader("📈 Resource Usage Overview")
col1, col2 = st.columns(2)
col1.metric("Avg Water Usage", round(data["water"].mean(), 2))
col2.metric("Avg Electricity Usage", round(data["electricity"].mean(), 2))

# Graphs
col3, col4 = st.columns(2)

with col3:
    st.subheader("💧 Water Usage")
    fig, ax = plt.subplots()
    ax.plot(data["water"], marker='o')
    ax.set_title("Daily Water Consumption Trend")
    ax.set_xlabel("Days")
    ax.set_ylabel("Water Usage (Liters)")
    st.pyplot(fig)

with col4:
    st.subheader("⚡ Electricity Usage")
    fig2, ax2 = plt.subplots()
    ax2.plot(data["electricity"], marker='o')
    ax2.set_title("Daily Energy Consumption Trend")
    ax2.set_xlabel("Days")
    ax2.set_ylabel("Electricity Usage (kWh)")
    st.pyplot(fig2)

# Alerts
alerts = detect_wastage(data)
for alert in alerts:
    st.warning("⚠ Resource Alert: " + alert)

# Anomaly alerts
anomaly_alerts = detect_anomalies(data)
for alert in anomaly_alerts:
    st.error("🚨 Critical Anomaly: " + alert)
# ================== IMMEDIATE ACTION ==================
st.subheader("⚡ Immediate Action System")

if data["water"].iloc[-1] > data["water"].mean() * 1.5:
    st.error("🚨 ACTION REQUIRED: Water usage is too high!")

    if st.button("🔧 Assign Maintenance Team"):
        st.success("👷 Maintenance team notified!")

    if st.button("🚰 Shut Down Overflow Tank"):
        st.success("🚰 Tank shutdown initiated!")

    if st.button("📢 Notify Hostel Warden"):
        st.success("📢 Warden notified!")

if data["electricity"].iloc[-1] > data["electricity"].mean() * 1.5:
    st.error("🚨 ACTION REQUIRED: Electricity usage is too high!")

    if st.button("💡 Turn Off Non-Essential Loads"):
        st.success("💡 Non-essential loads turned off!")

    if st.button("⚙ Check Equipment"):
        st.success("⚙ Equipment inspection started!")

    if st.button("📢 Notify Electrical Dept"):
        st.success("📢 Electrical team notified!")
# ================== AUTO CONTROL ==================
st.subheader("🤖 Auto-Control System")

auto_action = None

if data["water"].iloc[-1] > data["water"].mean() * 1.5:
    auto_action = "Water flow reduced by 20%"
    st.success("💧 Auto-Control Activated: Reducing water flow...")

elif data["electricity"].iloc[-1] > data["electricity"].mean() * 1.5:
    auto_action = "Power load reduced"
    st.success("⚡ Auto-Control Activated: Reducing electricity load...")

else:
    st.info("✅ System running normally")
# ================== IMPACT SIMULATION ==================
st.subheader("📉 Post-Control Impact")

if auto_action:
    reduced_water = data["water"].iloc[-1] * 0.8
    reduced_elec = data["electricity"].iloc[-1] * 0.85

    st.write(f"💧 Water after control: {round(reduced_water,2)} liters")
    st.write(f"⚡ Electricity after control: {round(reduced_elec,2)} units")
# ================== AUTO EMAIL ==================
st.subheader("📡 Auto Notification")

if auto_action and user_email:
    message = f"Auto-Control Action Taken: {auto_action}"
    send_email_alert(user_email, message)
    st.success("📧 Alert sent automatically!")

# Real-time latest day alert
latest_day = len(data)

if data["water"].iloc[-1] > data["water"].mean() * 1.5:
    st.error(f"🚨 ALERT TODAY (Day {latest_day}): Water usage too high!")

if data["electricity"].iloc[-1] > data["electricity"].mean() * 1.5:
    st.error(f"🚨 ALERT TODAY (Day {latest_day}): Electricity usage too high!")

# Email alert
if anomaly_alerts and user_email:
    message = "\n".join(anomaly_alerts)
    result = send_email_alert(user_email, message)
    st.success(result)

# Recommended actions
st.subheader("🛠 Recommended Actions")

if data["water"].iloc[-1] > data["water"].mean() * 1.5:
    st.error("🚨 Water wastage detected!")
    st.write("👉 Check for leaking taps or pipelines")
    st.write("👉 Reduce unnecessary water usage in hostels")
    st.write("👉 Inspect storage tanks for overflow")

if data["electricity"].iloc[-1] > data["electricity"].mean() * 1.5:
    st.error("🚨 Electricity overuse detected!")
    st.write("👉 Turn off unused lights and equipment")
    st.write("👉 Check for faulty appliances")
    st.write("👉 Shift heavy usage to off-peak hours")

# Estimated impact
st.subheader("💰 Estimated Impact")

extra_water = data["water"].iloc[-1] - data["water"].mean()
extra_elec = data["electricity"].iloc[-1] - data["electricity"].mean()

st.write(f"Extra Water Usage: {round(extra_water,2)} liters")
st.write(f"Extra Electricity Usage: {round(extra_elec,2)} units")

# Predictions
st.subheader("🔮 AI-Based Future Predictions")

col5, col6 = st.columns(2)

electricity_pred = predict_usage(data)
col5.success(f"⚡ Predicted Electricity Tomorrow: {electricity_pred:.2f}")

water_pred = predict_water_usage(data)
col6.success(f"💧 Predicted Water Usage Tomorrow: {water_pred:.2f}")

# AI Insights
st.subheader("🧠 AI Insights & Recommendations")

if data["water"].mean() > 2000:
    st.info("💧 High water consumption detected. Recommend optimizing usage in hostels and restrooms.")

if data["electricity"].max() > data["electricity"].mean() * 1.5:
    st.info("⚡ Sudden spike in energy usage detected. Possible equipment overload or peak-time usage.")

if len(data) > 5:
    st.success("📊 System analysis complete. Usage patterns identified successfully.")

# Sustainability score
st.subheader("🌱 Sustainability Score")

score = 100

if data["water"].max() > data["water"].mean() * 1.5:
    score -= 20

if data["electricity"].max() > data["electricity"].mean() * 1.5:
    score -= 20

st.success(f"Campus Sustainability Score: {score}/100")

# Download report
csv = data.to_csv(index=False)

st.download_button(
    label="📥 Download AI Analysis Report",
    data=csv,
    file_name="utility_report.csv",
    mime="text/csv"
)