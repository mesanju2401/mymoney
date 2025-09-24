import streamlit as st
from datetime import datetime
from utils.api_client import APIClient
from utils.validators import validate_amount

def transaction_form():
    """Render transaction form"""
    api_client = APIClient()
    
    with st.form("transaction_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            transaction_type = st.selectbox("Type", ["Expense", "Income"])
            amount = st.number_input("Amount", min_value=0.01, step=0.01)
            category = st.selectbox(
                "Category",
                ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Other"]
                if transaction_type == "Expense" else ["Salary", "Freelance", "Investment", "Other"]
            )
        
        with col2:
            date = st.date_input("Date", value=datetime.now())
            description = st.text_input("Description")
        
        submitted = st.form_submit_button("Add Transaction")
        
        if submitted:
            if validate_amount(amount):
                transaction = {
                    "amount": amount,
                    "category": category,
                    "description": description,
                    "transaction_type": transaction_type.lower(),
                    "date": date.isoformat()
                }
                
                result = api_client.add_transaction(transaction)
                if result:
                    st.success("Transaction added successfully!")
                    st.rerun()
                else:
                    st.error("Failed to add transaction")
            else:
                st.error("Please enter a valid amount")

def budget_form():
    """Render budget form"""
    api_client = APIClient()
    
    with st.form("budget_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            category = st.selectbox(
                "Category",
                ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Other"]
            )
            amount = st.number_input("Budget Amount", min_value=0.01, step=10.0)
        
        with col2:
            month = st.selectbox(
                "Month",
                [datetime.now().strftime("%Y-%m")],
                format_func=lambda x: datetime.strptime(x, "%Y-%m").strftime("%B %Y")
            )
        
        submitted = st.form_submit_button("Set Budget")
        
        if submitted:
            if validate_amount(amount):
                budget = {
                    "category": category,
                    "amount": amount,
                    "month": month
                }
                
                result = api_client.add_budget(budget)
                if result:
                    st.success("Budget set successfully!")
                    st.rerun()
                else:
                    st.error("Failed to set budget")
            else:
                st.error("Please enter a valid amount")
