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
# Convert category breakdown to dict for easy lookup
expense_by_category = {item['category']: item['total'] for item in category_breakdown} if category_breakdown else {}

if budgets:
    # Display budget cards
    cols = st.columns(3)
    for idx, budget in enumerate(budgets):
        with cols[idx % 3]:
            spent = expense_by_category.get(budget['category'], 0)
            budget_card(
                category=budget['category'],
                budget_amount=budget['amount'],
                spent_amount=spent,
                month=budget['month']
            )
else:
    st.info("No budgets set. Create your first budget above!")

# Budget summary
st.markdown("---")
st.subheader("Budget Summary")

if budgets:
    total_budget = sum(b['amount'] for b in budgets)
    total_spent = sum(expense_by_category.values())
    remaining = total_budget - total_spent
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Budget", format_currency(total_budget))
    
    with col2:
        st.metric("Total Spent", format_currency(total_spent))
    
    with col3:
        st.metric(
            "Remaining",
            format_currency(remaining),
            delta=f"{(remaining/total_budget*100):.1f}% left" if total_budget > 0 else "0%",
            delta_color="normal" if remaining >= 0 else "inverse"
        )
    
    # Progress bar
    progress = min(total_spent / total_budget, 1.0) if total_budget > 0 else 0
    st.progress(progress)
    
    if progress > 0.9:
        st.warning("⚠️ You've used over 90% of your budget!")
    elif progress > 1.0:
        st.error("🚨 You've exceeded your budget!")
# Convert category breakdown to dict for easy﻿ 
