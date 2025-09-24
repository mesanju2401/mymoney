import streamlit as st
from utils.session_manager import SessionManager
from components.navbar import render_navbar
from utils.api_client import APIClient
from utils.formatters import format_currency

st.set_page_config(
    page_title="MyMoney - Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session manager
session_manager = SessionManager()
api_client = APIClient()

# Check authentication
if not session_manager.is_authenticated():
    st.title("Welcome to MyMoney 💰")
    st.markdown("### Your Personal Finance Tracker")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                token = api_client.login(username, password)
                if token:
                    session_manager.login(username, token)
                    st.rerun()
                else:
                    st.error("Invalid credentials")
    
    with tab2:
        with st.form("register_form"):
            email = st.text_input("Email")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("Register")
            
            if submit:
                if password != confirm_password:
                    st.error("Passwords don't match")
                else:
                    user = api_client.register(email, username, password)
                    if user:
                        st.success("Registration successful! Please login.")
                    else:
                        st.error("Registration failed. Username or email may already exist.")
else:
    # Authenticated user view
    render_navbar()
    
    st.title("Dashboard")
    
    # Get current month summary
    import datetime
    current_month = datetime.datetime.now().strftime("%Y-%m")
    summary = api_client.get_monthly_summary(current_month)
    
    # Display summary cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Income",
            value=format_currency(summary.get("income", 0)),
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label="Expenses",
            value=format_currency(summary.get("expense", 0)),
            delta_color="inverse"
        )
    
    with col3:
        balance = summary.get("balance", 0)
        st.metric(
            label="Balance",
            value=format_currency(balance),
            delta=format_currency(balance),
            delta_color="normal" if balance >= 0 else "inverse"
        )
    
    # Recent transactions
    st.subheader("Recent Transactions")
    transactions = api_client.get_transactions(limit=5)
    
    if transactions:
        for transaction in transactions:
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"**{transaction['category']}** - {transaction['description']}")
                with col2:
                    st.write(transaction['date'][:10])
                with col3:
                    amount = transaction['amount']
                    if transaction['transaction_type'] == 'expense':
                        st.write(f"🔴 -{format_currency(amount)}")
                    else:
                        st.write(f"🟢 +{format_currency(amount)}")
    else:
        st.info("No transactions yet. Add your first transaction!")﻿ 
