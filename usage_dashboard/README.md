# WARNING: NOT TESTED

# 📘 Usage Dashboard

This project includes a lightweight analytics system that tracks visits to the Port of New Orleans Trade Dashboard. It requires no external database or API keys and stores all analytics in a local persistent file (`analytics.json`) inside the Streamlit app environment.

## 🔍 What the Usage Dashboard Shows

- Total visits
- Daily, monthly, and yearly active users
- Visitors by country and city (when location tracking is enabled)
- Time-of-day heatmap
- Geographic map of visitors
- Session trends over time

All analytics are computed from the local `analytics.json` file.

## 📁 Where Analytics Data Lives

Streamlit Community Cloud provides a private persistent filesystem for each deployed app.  
The analytics file is stored at:

`analytics.json`

This file persists across app restarts, is not synced to GitHub, and is only accessible to the app itself.

## 📝 How Data Gets Logged

Each time a user loads the dashboard, the app logs:

- a unique session ID
- timestamp
- (when deployed) country, city, region, timezone, IP
- (optional) latitude/longitude

Location tracking works only when deployed, because the JavaScript component does not run in local development mode.

## 📊 Viewing the Usage Dashboard

The usage dashboard is located at:

`pages/Usage Dashboard.py`

Streamlit automatically adds it to the sidebar. Open it to view charts, maps, and summary metrics.

## 🧹 Resetting Analytics

To reset analytics, delete:

`analytics.json`

It will be recreated automatically on the next visit.
