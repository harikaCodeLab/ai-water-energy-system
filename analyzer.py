import pandas as pd
from sklearn.linear_model import LinearRegression

def load_data():
    return pd.read_csv("data/usage.csv")

def detect_wastage(data):
    alerts = []

    if data["water"].max() > 800:
        alerts.append("⚠ High water usage detected")

    if data["electricity"].max() > 5:
        alerts.append("⚠ High electricity usage detected")

    return alerts

def predict_usage(data):
    from sklearn.linear_model import LinearRegression

    data = data.dropna()  # extra safety

    X = data.index.values.reshape(-1,1)
    y = data["electricity"]

    model = LinearRegression()
    model.fit(X, y)

    return model.predict([[len(data)+1]])[0]

def detect_anomalies(data):
    alerts = []

    avg_water = data["water"].mean()
    avg_elec = data["electricity"].mean()

    for i in range(1, len(data)):

        # Early warning (slight increase)
        if data["water"][i] > avg_water * 1.2:
            alerts.append(f"⚠ Water usage rising on Day {i+1}")

        # Critical spike
        if data["water"][i] > avg_water * 1.5:
            alerts.append(f"🚨 Water spike on Day {i+1}")

        if data["electricity"][i] > avg_elec * 1.2:
            alerts.append(f"⚠ Electricity usage rising on Day {i+1}")

        if data["electricity"][i] > avg_elec * 1.5:
            alerts.append(f"🚨 Electricity spike on Day {i+1}")

    return alerts
    return alerts
def predict_water_usage(data):
    from sklearn.linear_model import LinearRegression
    
    X = data.index.values.reshape(-1,1)
    y = data["water"]

    model = LinearRegression()
    model.fit(X, y)

    return model.predict([[len(data)+1]])[0]

import smtplib
from email.mime.text import MIMEText

def send_email_alert(to_email, message):
    from_email = "gajjalaharikareddy77@gmail.com"
    app_password = "uyxjttilevkjqxic"

    msg = MIMEText(message)
    msg["Subject"] = "🚨 Campus Utility Alert"
    msg["From"] = from_email
    msg["To"] = to_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_email, app_password)
        server.send_message(msg)
        server.quit()
        return "Email sent successfully!"
    except Exception as e:
        return f"Error: {e}"