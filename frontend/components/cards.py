import streamlit as st
from utils.formatters import format_currency

def metric_card(title, value, delta=None, delta_color="normal"):
    """Display a metric card"""
    container = st.container()
    with container:
        st.metric(label=title, value=value, delta=delta, delta_color=delta_color)
    return container

def budget_card(category, budget_amount, spent_amount, month):
    """Display a budget card with progress"""
    with st.container():
        st.markdown(f"### {category}")
        
        # Calculate percentage
        percentage = (spent_amount / budget_amount * 100) if budget_amount > 0 else 0
        remaining = budget_amount - spent_amount
        
        # Display metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Budget", format_currency(budget_amount))
        with col2:
            st.metric("Spent", format_currency(spent_amount))
        
        # Progress bar
        progress_color = "normal"
        if percentage > 90:
            progress_color = "🔴"
        elif percentage > 70:
            progress_color = "🟡"
        else:
            progress_color = "🟢"
        
        st.progress(min(percentage / 100, 1.0))
        st.caption(f"{progress_color} {percentage:.1f}% used • {format_currency(remaining)} remaining")
