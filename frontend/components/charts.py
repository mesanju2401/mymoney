import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

def expense_pie_chart(category_data):
    """Create expense breakdown pie chart"""
    df = pd.DataFrame(category_data)
    
    fig = px.pie(
        df, 
        values='total', 
        names='category',
        title='Expense Distribution',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

def category_bar_chart(category_data):
    """Create category comparison bar chart"""
    df = pd.DataFrame(category_data)
    
    fig = px.bar(
        df,
        x='category',
        y='total',
        title='Spending by Category',
        color='total',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

def monthly_trend_chart(transactions):
    """Create monthly trend line chart"""
    if not transactions:
        st.info("Not enough data for trend analysis")
        return
    
    df = pd.DataFrame(transactions)
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M').astype(str)
    
    # Group by month and type
    monthly_summary = df.groupby(['month', 'transaction_type'])['amount'].sum().reset_index()
    
    # Create line chart
    fig = go.Figure()
    
    for trans_type in ['income', 'expense']:
        data = monthly_summary[monthly_summary['transaction_type'] == trans_type]
        fig.add_trace(go.Scatter(
            x=data['month'],
            y=data['amount'],
            mode='lines+markers',
            name=trans_type.capitalize(),
            line=dict(width=3)
        ))
    
    fig.update_layout(
        title='Income vs Expenses Trend',
        xaxis_title='Month',
        yaxis_title='Amount',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
