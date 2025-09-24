 import streamlit as st
from utils.session_manager import SessionManager
from utils.api_client import APIClient
from components.navbar import render_navbar

st.set_page_config(page_title="Settings - MyMoney", page_icon="💰", layout="wide")

# Load custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

session_manager = SessionManager()
api_client = APIClient()

if not session_manager.is_authenticated():
    st.error("Please login to access this page")
    st.stop()

render_navbar()
st.title("Settings")

# User info
user_info = api_client.get_current_user()

st.subheader("Profile Information")
col1, col2 = st.columns(2)

with col1:
    st.text_input("Username", value=user_info.get('username', ''), disabled=True)
    st.text_input("Email", value=user_info.get('email', ''), disabled=True)

with col2:
    st.text_input("Member Since", value=user_info.get('created_at', '')[:10], disabled=True)
    st.text_input("Status", value="Active" if user_info.get('is_active') else "Inactive", disabled=True)

st.markdown("---")

# Preferences
st.subheader("Preferences")

col1, col2 = st.columns(2)

with col1:
    currency = st.selectbox("Currency", ["USD ($)", "EUR (€)", "GBP (£)", "INR (₹)"])
    date_format = st.selectbox("Date Format", ["MM/DD/YYYY", "DD/MM/YYYY", "YYYY-MM-DD"])

with col2:
    theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
    notifications = st.checkbox("Email Notifications", value=True)

if st.button("Save Preferences"):
    st.success("Preferences saved successfully!")

st.markdown("---")

# Danger Zone
st.subheader("Danger Zone")

col1, col2 = st.columns(2)

with col1:
    if st.button("Export Data", type="secondary"):
        st.info("Feature coming soon!")

with col2:
    if st.button("Delete Account", type="secondary"):
        st.warning("This action cannot be undone!")

# Logout button
st.markdown("---")
if st.button("Logout", type="primary"):
    session_manager.logout()
    st.rerun()
