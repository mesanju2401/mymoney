"""
Card components for the Personal Finance Tracker application.

This module contains functions to create various types of cards for displaying
metrics, summaries, and information in a visually appealing format.
"""

import streamlit as st
from typing import Optional, Union

def create_metric_card(
    title: str,
    value: Union[int, float, str],
    delta: Optional[Union[int, float, str]] = None,
    delta_color: str = "normal",
    background_gradient: str = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    text_color: str = "white"
) -> None:
    """
    Create a metric card with value and optional delta.
    
    Args:
        title: The title/label for the metric
        value: The main value to display
        delta: Optional delta/change value
        delta_color: Color for delta (normal, inverse, off)
        background_gradient: CSS gradient for background
        text_color: Text color for the card
    """
    delta_html = ""
    if delta is not None:
        delta_sign = "+" if str(delta).replace("-", "").replace(".", "").isdigit() and float(delta) > 0 else ""
        delta_html = f'<div style="font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.9;">{delta_sign}{delta}</div>'
    
    card_html = f"""
    <div style="
        background: {background_gradient};
        padding: 1.5rem;
        border-radius: 10px;
        color: {text_color};
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    ">
        <div style="font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem;">{value}</div>
        <div style="font-size: 0.9rem; opacity: 0.9;">{title}</div>
        {delta_html}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

def create_summary_card(
    title: str,
    items: list,
    background_color: str = "#f8f9fa",
    border_color: str = "#dee2e6"
) -> None:
    """
    Create a summary card with a list of items.
    
    Args:
        title: Card title
        items: List of items to display
        background_color: Background color for the card
        border_color: Border color for the card
    """
    items_html = ""
    for item in items:
        if isinstance(item, dict):
            label = item.get('label', '')
            value = item.get('value', '')
            items_html += f'<div style="margin: 0.5rem 0;"><strong>{label}:</strong> {value}</div>'
        else:
            items_html += f'<div style="margin: 0.5rem 0;">• {item}</div>'
    
    card_html = f"""
    <div style="
        background-color: {background_color};
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid {border_color};
        margin-bottom: 1rem;
    ">
        <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 1rem; color: #495057;">{title}</div>
        {items_html}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

def create_info_card(
    title: str,
    content: str,
    icon: str = "ℹ️",
    card_type: str = "info"
) -> None:
    """
    Create an information card with different styles based on type.
    
    Args:
        title: Card title
        content: Card content/message
        icon: Icon to display
        card_type: Type of card (info, success, warning, error)
    """
    colors = {
        "info": {"bg": "#d1ecf1", "border": "#bee5eb", "text": "#0c5460"},
        "success": {"bg": "#d4edda", "border": "#c3e6cb", "text": "#155724"},
        "warning": {"bg": "#fff3cd", "border": "#ffeaa7", "text": "#856404"},
        "error": {"bg": "#f8d7da", "border": "#f5c6cb", "text": "#721c24"}
    }
    
    color_scheme = colors.get(card_type, colors["info"])
    
    card_html = f"""
    <div style="
        background-color: {color_scheme['bg']};
        color: {color_scheme['text']};
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid {color_scheme['border']};
        margin: 1rem 0;
    ">
        <div style="font-weight: 600; margin-bottom: 0.5rem;">
            {icon} {title}
        </div>
        <div>{content}</div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

def create_transaction_card(
    transaction_data: dict,
    show_delete: bool = False,
    card_key: str = ""
) -> bool:
    """
    Create a card for displaying transaction information.
    
    Args:
        transaction_data: Dictionary containing transaction data
        show_delete: Whether to show delete button
        card_key: Unique key for the card
        
    Returns:
        bool: True if delete button was clicked
    """
    transaction_type = transaction_data.get('type', 'Expense')
    amount = transaction_data.get('amount', 0)
    description = transaction_data.get('description', '')
    category = transaction_data.get('category', '')
    date = transaction_data.get('date', '')
    
    # Color scheme based on transaction type
    if transaction_type == 'Income':
        bg_color = "#d4edda"
        border_color = "#c3e6cb"
        amount_color = "#28a745"
    else:
        bg_color = "#f8d7da"
        border_color = "#f5c6cb"
        amount_color = "#dc3545"
    
    # Format amount
    amount_str = f"₹{abs(amount):,.2f}"
    if transaction_type == 'Expense':
        amount_str = f"-{amount_str}"
    
    col1, col2, col3, col4, col5 = st.columns([2, 3, 2, 2, 1])
    
    with col1:
        st.write(f"**{date}**")
    
    with col2:
        st.write(description)
    
    with col3:
        st.write(category)
    
    with col4:
        st.markdown(f"<span style='color: {amount_color}; font-weight: bold;'>{amount_str}</span>", 
                   unsafe_allow_html=True)
    
    with col5:
        if show_delete:
            return st.button("🗑️", key=f"delete_{card_key}", help="Delete transaction")
    
    return False

def create_budget_progress_card(
    category: str,
    spent: float,
    budget: float,
    period: str = "monthly"
) -> None:
    """
    Create a budget progress card showing spending vs budget.
    
    Args:
        category: Budget category name
        spent: Amount spent
        budget: Budget limit
        period: Budget period (monthly, weekly, etc.)
    """
    percentage = (spent / budget * 100) if budget > 0 else 0
    remaining = budget - spent
    
    # Color based on percentage
    if percentage <= 50:
        progress_color = "#28a745"  # Green
    elif percentage <= 80:
        progress_color = "#ffc107"  # Yellow
    else:
        progress_color = "#dc3545"  # Red
    
    card_html = f"""
    <div style="
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid {progress_color};
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    ">
        <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
            <div style="font-weight: 600; color: #495057;">{category}</div>
            <div style="color: #6c757d; font-size: 0.9rem;">{period}</div>
        </div>
        
        <div style="margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="color: #6c757d;">Spent: ₹{spent:,.2f}</span>
                <span style="color: #6c757d;">Budget: ₹{budget:,.2f}</span>
            </div>
            <div style="
                width: 100%; 
                background-color: #e9ecef; 
                border-radius: 10px; 
                height: 10px;
                overflow: hidden;
            ">
                <div style="
                    width: {min(percentage, 100)}%; 
                    background-color: {progress_color}; 
                    height: 100%;
                    border-radius: 10px;
                    transition: width 0.3s ease;
                "></div>
            </div>
        </div>
        
        <div style="display: flex; justify-content: space-between; font-size: 0.9rem;">
            <span style="color: {progress_color}; font-weight: bold;">{percentage:.1f}% used</span>
            <span style="color: {'#28a745' if remaining >= 0 else '#dc3545'};">
                ₹{abs(remaining):,.2f} {'remaining' if remaining >= 0 else 'over budget'}
            </span>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)﻿ 
