import streamlit as st
import pandas as pd
from utils.session_manager import SessionManager
from utils.api_client import APIClient
from components.charts import expense_pie_chart, monthly_trend_chart, category_bar_chart
from components.navbar import render_navbar
import datetime

st.set_page_config(page_title="Analytics - MyMoney", page_icon="💰", layout="wide")

# Load custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

session_manager = SessionManager()
api_client = APIClient()

if not session_manager.is_authenticated():
    st.error("Please login to access this page")
    st.stop()

render_navbar()
st.title("Analytics & Insights")

# Month selector
current_month = datetime.datetime.now().strftime("%Y-%m")
selected_month = st.selectbox(
    "Select Month",
    options=[current_month],  # You can expand this
    format_func=lambda x: datetime.datetime.strptime(x, "%Y-%m").strftime("%B %Y")
)

# Get data
summary = api_client.get_monthly_summary(selected_month)
category_breakdown = api_client.get_category_breakdown(selected_month)

# Summary metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Income", f"${summary.get('income', 0):,.2f}")

with col2:
    st.metric("Total Expenses", f"${summary.get('expense', 0):,.2f}")

with col3:
    balance = summary.get('balance', 0)
    st.metric("Net Balance", f"${balance:,.2f}", 
              delta=f"${balance:,.2f}",
              delta_color="normal" if balance >= 0 else "inverse")

with col4:
    savings_rate = (summary.get('income', 0) - summary.get('expense', 0)) / summary.get('income', 1) * 100 if summary.get('income', 0) > 0 else 0
    st.metric("Savings Rate", f"{savings_rate:.1f}%")

# Charts
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Expense Breakdown by Category")
    if category_breakdown:
        expense_pie_chart(category_breakdown)
    else:
        st.info("No expenses recorded for this month")

with col2:
    st.subheader("Category Comparison")
    if category_breakdown:
        category_bar_chart(category_breakdown)
    else:
        st.info("No expenses recorded for this month")

# Monthly trend (placeholder - would need more data)
st.subheader("Monthly Trend")
monthly_trend_chart(api_client.get_transactions())﻿ 
