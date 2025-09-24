import streamlit as st
from utils.session_manager import SessionManager
from utils.api_client import APIClient
from components.forms import budget_form
from components.cards import budget_card
from components.navbar import render_navbar
from utils.formatters import format_currency
import datetime

st.set_page_config(page_title="Budget - MyMoney", page_icon="💰", layout="wide")

# Load custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

session_manager = SessionManager()
api_client = APIClient()

if not session_manager.is_authenticated():
    st.error("Please login to access this page")
    st.stop()

render_navbar()
st.title("Budget Management")

current_month = datetime.datetime.now().strftime("%Y-%m")

# Add budget section
with st.expander("Set Budget Goals", expanded=True):
    budget_form()

# Display budgets
st.subheader(f"Budget Overview - {datetime.datetime.now().strftime('%B %Y')}")

budgets = api_client.get_budgets()
category_breakdown = api_client.get_category_breakdown(current_month)

# Convert category breakdown to dict for easy﻿ 
