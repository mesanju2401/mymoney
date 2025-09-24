"""
Chart components for the Personal Finance Tracker application.

This module contains functions to create various types of charts and visualizations
using Plotly for financial data analysis.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Optional, List, Dict, Any

def create_expense_pie_chart(
    data: pd.DataFrame,
    title: str = "Expense Breakdown by Category",
    hole_size: float = 0.4,
    height: int = 400
) -> go.Figure:
    """
    Create a pie chart for expense breakdown by category.
    
    Args:
        data: DataFrame with expense data
        title: Chart title
        hole_size: Size of center hole (0 for no hole, 0.5 for donut)
        height: Chart height in pixels
        
    Returns:
        Plotly figure object
    """
    # Filter expense data and group by category
    expense_data = data[data['type'] == 'Expense'].copy()
    
    if expense_data.empty:
        # Return empty chart with message
        fig = go.Figure()
        fig.add_annotation(
            text="No expense data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False, font=dict(size=16, color="gray")
        )
        fig.update_layout(height=height, title=title)
        return fig
    
    # Group by category and sum amounts (make positive)
    category_totals = expense_data.groupby('category')['amount'].sum().abs()
    
    # Create pie chart
    fig = px.pie(
        values=category_totals.values,
        names=category_totals.index,
        title=title,
        color_discrete_sequence=px.colors.qualitative.Set3,
        hole=hole_size
    )
    
    # Update layout
    fig.update_traces(
        textposition='auto',
        textinfo='percent+label',
        textfont_size=12,
        hovertemplate="<b>%{label}</b><br>" +
                     "Amount: ₹%{value:,.2f}<br>" +
                     "Percentage: %{percent}<br>" +
                     "<extra></extra>"
    )
    
    fig.update_layout(
        height=height,
        showlegend=True,
        title_font_size=16,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05
        )
    )
    
    return fig

def create_income_vs_expense_chart(
    data: pd.DataFrame,
    period: str = "monthly",
    title: Optional[str] = None,
    height: int = 400
) -> go.Figure:
    """
    Create a line chart comparing income vs expenses over time.
    
    Args:
        data: DataFrame with transaction data
        period: Time period for grouping (monthly, weekly, daily)
        title: Chart title
        height: Chart height in pixels
        
    Returns:
        Plotly figure object
    """
    if title is None:
        title = f"Income vs Expenses ({period.title()})"
    
    # Prepare data based on period
    df = data.copy()
    
    if period == "monthly":
        df['period'] = df['date'].dt.to_period('M').astype(str)
    elif period == "weekly":
        df['period'] = df['date'].dt.to_period('W').astype(str)
    elif period == "daily":
        df['period'] = df['date'].dt.date.astype(str)
    else:
        df['period'] = df['date'].dt.to_period('M').astype(str)
    
    # Group by period and type
    summary = df.groupby(['period', 'type'])['amount'].sum().reset_index()
    
    if summary.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available for the selected period",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False, font=dict(size=16, color="gray")
        )
        fig.update_layout(height=height, title=title)
        return fig
    
    # Create line chart
    fig = px.line(
        summary,
        x='period',
        y='amount',
        color='type',
        title=title,
        markers=True,
        line_shape='spline'
    )
    
    # Update traces
    fig.update_traces(
        line=dict(width=3),
        hovertemplate="<b>%{fullData.name}</b><br>" +
                     "Period: %{x}<br>" +
                     "Amount: ₹%{y:,.2f}<br>" +
                     "<extra></extra>"
    )
    
    # Update layout
    fig.update_layout(
        height=height,
        title_font_size=16,
        xaxis_title=period.title(),
        yaxis_title='Amount (₹)',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_monthly_trend_chart(
    data: pd.DataFrame,
    title: str = "Monthly Financial Trend",
    height: int = 400
) -> go.Figure:
    """
    Create a combination chart showing monthly income, expenses, and savings.
    
    Args:
        data: DataFrame with transaction data
        title: Chart title
        height: Chart height in pixels
        
    Returns:
        Plotly figure object
    """
    # Prepare monthly data
    df = data.copy()
    df['month'] = df['date'].dt.to_period('M').astype(str)
    
    # Group by month and type
    monthly_summary = df.groupby(['month', 'type'])['amount'].sum().reset_index()
    
    if monthly_summary.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False, font=dict(size=16, color="gray")
        )
        fig.update_layout(height=height, title=title)
        return fig
    
    # Pivot data
    pivot_data = monthly_summary.pivot(index='month', columns='type', values='amount').fillna(0)
    
    # Calculate savings
    if 'Income' in pivot_data.columns and 'Expense' in pivot_data.columns:
        pivot_data['Savings'] = pivot_data['Income'] + pivot_data['Expense']  # Expense is negative
    else:
        pivot_data['Savings'] = 0
    
    # Create figure with secondary y-axis
    fig = go.Figure()
    
    # Add income and expense bars
    if 'Income' in pivot_data.columns:
        fig.add_trace(go.Bar(
            name='Income',
            x=pivot_data.index,
            y=pivot_data['Income'],
            marker_color='#28a745',
            hovertemplate="<b>Income</b><br>" +
                         "Month: %{x}<br>" +
                         "Amount: ₹%{y:,.2f}<br>" +
                         "<extra></extra>"
        ))
    
    if 'Expense' in pivot_data.columns:
        fig.add_trace(go.Bar(
            name='Expenses',
            x=pivot_data.index,
            y=pivot_data['Expense'].abs(),  # Show as positive for better visualization
            marker_color='#dc3545',
            hovertemplate="<b>Expenses</b><br>" +
                         "Month: %{x}<br>" +
                         "Amount: ₹%{y:,.2f}<br>" +
                         "<extra></extra>"
        ))
    
    # Add savings line
    fig.add_trace(go.Scatter(
        name='Savings',
        x=pivot_data.index,
        y=pivot_data['Savings'],
        mode='lines+markers',
        line=dict(color='#17a2b8', width=3),
        marker=dict(size=8),
        yaxis='y2',
        hovertemplate="<b>Savings</b><br>" +
                     "Month: %{x}<br>" +
                     "Amount: ₹%{y:,.2f}<br>" +
                     "<extra></extra>"
    ))
    
    # Update layout
    fig.update_layout(
        title=title,
        title_font_size=16,
        xaxis_title='Month',
        yaxis_title='Amount (₹)',
        yaxis2=dict(
            title='Savings (₹)',
            overlaying='y',
            side='right'
        ),
        height=height,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_category_bar_chart(
    data: pd.DataFrame,
    transaction_type: str = "Expense",
    title: Optional[str] = None,
    top_n: int = 10,
    height: int = 400,
    orientation: str = "h"
) -> go.Figure:
    """
    Create a bar chart showing spending/income by category.
    
    Args:
        data: DataFrame with transaction data
        transaction_type: Type of transaction (Income/Expense)
        title: Chart title
        top_n: Number of top categories to show
        height: Chart height in pixels
        orientation: Chart orientation (h for horizontal, v for vertical)
        
    Returns:
        Plotly figure object
    """
    if title is None:
        title = f"Top {top_n} {transaction_type} Categories"
    
    # Filter data by type
    filtered_data = data[data['type'] == transaction_type].copy()
    
    if filtered_data.empty:
        fig = go.Figure()
        fig.add_annotation(
            text=f"No {transaction_type.lower()} data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False, font=dict(size=16, color="gray")
        )
        fig.update_layout(height=height, title=title)
        return fig
    
    # Group by category and sum amounts
    category_totals = filtered_data.groupby('category')['amount'].sum()
    
    if transaction_type == "Expense":
        category_totals = category_totals.abs()
    
    # Get top N categories
    top_categories = category_totals.nlargest(top_n)
    
    # Create bar chart
    if orientation == "h":
        fig = px.bar(
            x=top_categories.values,
            y=top_categories.index,
            orientation='h',
            title=title,
            labels={'x': 'Amount (₹)', 'y': 'Category'},
            color=top_categories.values,
            color_continuous_scale='Viridis' if transaction_type == 'Income' else 'Reds'
        )
        
        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            xaxis_title='Amount (₹)',
            yaxis_title='Category'
        )
    else:
        fig = px.bar(
            x=top_categories.index,
            y=top_categories.values,
            title=title,
            labels={'x': 'Category', 'y': 'Amount (₹)'},
            color=top_categories.values,
            color_continuous_scale='Viridis' if transaction_type == 'Income' else 'Reds'
        )
        
        fig.update_layout(
            xaxis={'categoryorder': 'total descending'},
            xaxis_title='Category',
            yaxis_title='Amount (₹)'
        )
    
    # Update layout
    fig.update_layout(
        height=height,
        title_font_size=16,
        showlegend=False
    )
    
    # Update traces
    fig.update_traces(
        hovertemplate="<b>%{" + ("y" if orientation == "h" else "x") + "}</b><br>" +
                     "Amount: ₹%{" + ("x" if orientation == "h" else "y") + ":,.2f}<br>" +
                     "<extra></extra>"
    )
    
    return fig

def create_spending_pattern_heatmap(
    data: pd.DataFrame,
    title: str = "Spending Patterns by Day of Week and Hour",
    height: int = 400
) -> go.Figure:
    """
    Create a heatmap showing spending patterns by day of week and hour.
    
    Args:
        data: DataFrame with transaction data
        title: Chart title
        height: Chart height in pixels
        
    Returns:
        Plotly figure object
    """
    # Filter expense data
    expense_data = data[data['type'] == 'Expense'].copy()
    
    if expense_data.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No expense data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False, font=dict(size=16, color="gray")
        )
        fig.update_layout(height=height, title=title)
        return fig
    
    # Extract day of week and hour
    expense_data['day_of_week'] = expense_data['date'].dt.day_name()
    expense_data['hour'] = expense_data['date'].dt.hour
    
    # Group by day and hour
    heatmap_data = expense_data.groupby(['day_of_week', 'hour'])['amount'].sum().abs()
    heatmap_pivot = heatmap_data.unstack(level=1, fill_value=0)
    
    # Reorder days
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_pivot = heatmap_pivot.reindex(day_order)
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_pivot.values,
        x=[f"{i:02d}:00" for i in range(24)],
        y=heatmap_pivot.index,
        colorscale='Reds',
        hoverongaps=False,
        hovertemplate="<b>%{y}</b><br>" +
                     "Hour: %{x}<br>" +
                     "Total Spent: ₹%{z:,.2f}<br>" +
                     "<extra></extra>"
    ))
    
    fig.update_layout(
        title=title,
        title_font_size=16,
        xaxis_title='Hour of Day',
        yaxis_title='Day of Week',
        height=height
    )
    
    return fig﻿ 
