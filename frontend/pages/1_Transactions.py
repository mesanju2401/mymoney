import streamlit as st
import pandas as pd
from utils.session_manager import SessionManager
from utils.api_client import APIClient
from components.forms import transaction_form
from utils.formatters import format_currency, format_date
from components.navbar import render_navbar

st.set_page_config(page_title="Transactions - MyMoney", page_icon="💰", layout="wide")

# Load custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

session_manager = SessionManager()
api_client = APIClient()

if not session_manager.is_authenticated():
    st.error("Please login to access this page")
    st.stop()

render_navbar()
st.title("Transactions")

# Add transaction section
with st.expander("Add New Transaction", expanded=True):
    transaction_form()

# Transaction list
st.subheader("Transaction History")

# Filters
col1, col2, col3 = st.columns(3)
with col1:
    filter_type = st.selectbox("Type", ["All", "Income", "Expense"])
with col2:
    filter_category = st.selectbox("Category", ["All"] + api_client.get_categories())
with col3:
    filter_month = st.selectbox("Month", ["All", "This Month", "Last Month"])

# Get and display transactions
transactions = api_client.get_transactions()

if transactions:
    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(transactions)
    
    # Apply filters
    if filter_type != "All":
        df = df[df['transaction_type'] == filter_type.lower()]
    
    # Display as a nice table
    for idx, row in df.iterrows():
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])
            
            with col1:
                st.write(f"**{row['category']}**")
                st.write(f"_{row['description']}_")
            
            with col2:
                st.write(format_date(row['date']))
            
            with col3:
                if row['transaction_type'] == 'expense':
                    st.write(f"🔴 Expense")
                else:
                    st.write(f"🟢 Income")
            
            with col4:
                amount = row['amount']
                if row['transaction_type'] == 'expense':
                    st.write(f"**-{format_currency(amount)}**")
                else:
                    st.write(f"**+{format_currency(amount)}**")
            
            with col5:
                if st.button("🗑️", key=f"delete_{row['id']}"):
                    if api_client.delete_transaction(row['id']):
                        st.success("Transaction deleted")
                        st.rerun()
else:
    st.info("No transactions found. Add your first transaction above!")﻿ 
