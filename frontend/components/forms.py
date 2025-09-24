"""
Form components for the Personal Finance Tracker application.

This module contains functions to create various forms for user input
including transaction forms, budget forms, and filter forms.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
from typing import Dict, List, Optional, Any, Tuple

def create_transaction_form(
    key_prefix: str = "transaction",
    default_values: Optional[Dict[str, Any]] = None
) -> Optional[Dict[str, Any]]:
    """
    Create a form for adding new transactions.
    
    Args:
        key_prefix: Prefix for form element keys
        default_values: Default values for form fields
        
    Returns:
        Dictionary with transaction data if submitted, None otherwise
    """
    if default_values is None:
        default_values = {}
    
    with st.form(key=f"{key_prefix}_form"):
        st.subheader("💰 Add New Transaction")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            transaction_date = st.date_input(
                "Date",
                value=default_values.get('date', date.today()),
                max_value=date.today(),
                key=f"{key_prefix}_date"
            )
            
            transaction_type = st.selectbox(
                "Type",
                ["Income", "Expense"],
                index=0 if default_values.get('type', 'Expense') == 'Income' else 1,
                key=f"{key_prefix}_type"
            )
        
        with col2:
            description = st.text_input(
                "Description",
                value=default_values.get('description', ''),
                placeholder="Enter transaction description",
                key=f"{key_prefix}_description"
            )
            
            # Dynamic categories based on transaction type
            categories = {
                "Income": ["Salary", "Freelance", "Investment", "Gift", "Bonus", "Other Income"],
                "Expense": ["Food", "Transportation", "Entertainment", "Bills", "Shopping", 
                           "Healthcare", "Education", "Rent", "Utilities", "Other"]
            }
            
            available_categories = categories[transaction_type]
            default_category = default_values.get('category', available_categories[0])
            
            category = st.selectbox(
                "Category",
                available_categories,
                index=available_categories.index(default_category) if default_category in available_categories else 0,
                key=f"{key_prefix}_category"
            )
        
        with col3:
            amount = st.number_input(
                "Amount (₹)",
                min_value=0.01,
                value=float(default_values.get('amount', 0.01)),
                step=0.01,
                format="%.2f",
                key=f"{key_prefix}_amount"
            )
            
            # Optional notes
            notes = st.text_area(
                "Notes (Optional)",
                value=default_values.get('notes', ''),
                placeholder="Additional notes...",
                max_chars=200,
                key=f"{key_prefix}_notes"
            )
        
        # Submit button
        submitted = st.form_submit_button("💾 Add Transaction", type="primary")
        
        if submitted:
            if description.strip() and amount > 0:
                # Adjust amount sign based on type
                final_amount = amount if transaction_type == "Income" else -amount
                
                transaction_data = {
                    'date': pd.Timestamp(transaction_date),
                    'description': description.strip(),
                    'amount': final_amount,
                    'category': category,
                    'type': transaction_type,
                    'notes': notes.strip()
                }
                
                return transaction_data
            else:
                st.error("Please fill in all required fields with valid data.")
                return None
    
    return None

def create_budget_form(
    key_prefix: str = "budget",
    existing_budgets: Optional[pd.DataFrame] = None
) -> Optional[Dict[str, Any]]:
    """
    Create a form for setting budget limits.
    
    Args:
        key_prefix: Prefix for form element keys
        existing_budgets: DataFrame with existing budget data
        
    Returns:
        Dictionary with budget data if submitted, None otherwise
    """
    with st.form(key=f"{key_prefix}_form"):
        st.subheader("💼 Set Budget Limit")
        
        col1, col2 = st.columns(2)
        
        with col1:
            categories = [
                "Food", "Transportation", "Entertainment", "Bills", "Shopping",
                "Healthcare", "Education", "Rent", "Utilities", "Other"
            ]
            
            category = st.selectbox(
                "Category",
                categories,
                key=f"{key_prefix}_category"
            )
            
            period = st.selectbox(
                "Budget Period",
                ["Monthly", "Weekly", "Daily"],
                key=f"{key_prefix}_period"
            )
        
        with col2:
            budget_amount = st.number_input(
                "Budget Amount (₹)",
                min_value=1.0,
                step=1.0,
                format="%.2f",
                key=f"{key_prefix}_amount"
            )
            
            # Show existing budget if any
            if existing_budgets is not None and not existing_budgets.empty:
                existing = existing_budgets[
                    (existing_budgets['category'] == category) & 
                    (existing_budgets['period'] == period)
                ]
                
                if not existing.empty:
                    current_budget = existing.iloc[0]['amount']
                    st.info(f"Current {period.lower()} budget for {category}: ₹{current_budget:,.2f}")
        
        # Additional settings
        st.subheader("⚙️ Budget Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            alert_threshold = st.slider(
                "Alert when % of budget is reached",
                min_value=50,
                max_value=100,
                value=80,
                step=5,
                key=f"{key_prefix}_threshold"
            )
        
        with col2:
            auto_reset = st.checkbox(
                "Auto-reset budget each period",
                value=True,
                key=f"{key_prefix}_auto_reset"
            )
        
        # Submit button
        submitted = st.form_submit_button("💾 Set Budget", type="primary")
        
        if submitted:
            if budget_amount > 0:
                budget_data = {
                    'category': category,
                    'period': period,
                    'amount': budget_amount,
                    'alert_threshold': alert_threshold,
                    'auto_reset': auto_reset,
                    'created_date': datetime.now()
                }
                
                return budget_data
            else:
                st.error("Please enter a valid budget amount.")
                return None
    
    return None

def create_filter_form(
    data: pd.DataFrame,
    key_prefix: str = "filter"
) -> Dict[str, Any]:
    """
    Create a form for filtering transactions.
    
    Args:
        data: DataFrame containing transaction data
        key_prefix: Prefix for form element keys
        
    Returns:
        Dictionary with filter parameters
    """
    st.subheader("🔍 Filter Options")
    
    with st.expander("Advanced Filters", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Transaction type filter
            transaction_types = ["All"] + list(data['type'].unique()) if not data.empty else ["All"]
            selected_type = st.selectbox(
                "Transaction Type",
                transaction_types,
                key=f"{key_prefix}_type"
            )
            
            # Amount range filter
            if not data.empty:
                min_amount = float(data['amount'].min())
                max_amount = float(data['amount'].max())
                
                amount_range = st.slider(
                    "Amount Range (₹)",
                    min_value=min_amount,
                    max_value=max_amount,
                    value=(min_amount, max_amount),
                    step=1.0,
                    key=f"{key_prefix}_amount_range"
                )
            else:
                amount_range = (0.0, 1000.0)
        
        with col2:
            # Category filter
            categories = ["All"] + list(data['category'].unique()) if not data.empty else ["All"]
            selected_categories = st.multiselect(
                "Categories",
                categories,
                default=["All"],
                key=f"{key_prefix}_categories"
            )
            
            # Description search
            description_search = st.text_input(
                "Search in Description",
                placeholder="Enter keywords...",
                key=f"{key_prefix}_description"
            )
        
        with col3:
            # Date range filter
            if not data.empty:
                min_date = data['date'].min().date()
                max_date = data['date'].max().date()
            else:
                min_date = date.today() - pd.Timedelta(days=30)
                max_date = date.today()
            
            date_range = st.date_input(
                "Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
                key=f"{key_prefix}_date_range"
            )
            
            # Sort options
            sort_by = st.selectbox(
                "Sort by",
                ["Date (Newest)", "Date (Oldest)", "Amount (High to Low)", "Amount (Low to High)", "Category"],
                key=f"{key_prefix}_sort"
            )
    
    # Quick filter buttons
    st.subheader("🚀 Quick Filters")
    
    col1, col2, col3, col4 = st.columns(4)
    
    quick_filters = {}
    
    with col1:
        quick_filters['this_month'] = st.button("This Month", key=f"{key_prefix}_this_month")
    
    with col2:
        quick_filters['last_month'] = st.button("Last Month", key=f"{key_prefix}_last_month")
    
    with col3:
        quick_filters['this_year'] = st.button("This Year", key=f"{key_prefix}_this_year")
    
    with col4:
        quick_filters['high_amounts'] = st.button("High Amounts (>₹1000)", key=f"{key_prefix}_high_amounts")
    
    # Return filter parameters
    filter_params = {
        'transaction_type': selected_type,
        'categories': selected_categories,
        'amount_range': amount_range,
        'date_range': date_range if len(date_range) == 2 else (min_date, max_date),
        'description_search': description_search.strip().lower(),
        'sort_by': sort_by,
        'quick_filters': quick_filters
    }
    
    return filter_params

def create_import_form(key_prefix: str = "import") -> Optional[pd.DataFrame]:
    """
    Create a form for importing transaction data from CSV.
    
    Args:
        key_prefix: Prefix for form element keys
        
    Returns:
        DataFrame with imported data if successful, None otherwise
    """
    st.subheader("📥 Import Transactions")
    
    with st.form(key=f"{key_prefix}_form"):
        uploaded_file = st.file_uploader(
            "Choose CSV file",
            type=['csv'],
            key=f"{key_prefix}_file"
        )
        
        if uploaded_file is not None:
            # CSV format options
            st.subheader("📋 CSV Format Options")
            
            col1, col2 = st.columns(2)
            
            with col1:
                delimiter = st.selectbox(
                    "Delimiter",
                    [",", ";", "\t", "|"],
                    key=f"{key_prefix}_delimiter"
                )
                
                has_header = st.checkbox(
                    "First row contains headers",
                    value=True,
                    key=f"{key_prefix}_header"
                )
            
            with col2:
                date_format = st.selectbox(
                    "Date Format",
                    ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y"],
                    key=f"{key_prefix}_date_format"
                )
        
        # Column mapping
        if uploaded_file is not None:
            st.subheader("🔗 Column Mapping")
            st.write("Map your CSV columns to the required fields:")
            
            try:
                # Read a sample of the CSV to show available columns
                sample_df = pd.read_csv(uploaded_file, nrows=5, delimiter=delimiter, header=0 if has_header else None)
                available_columns = [""] + list(sample_df.columns)
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    date_column = st.selectbox("Date Column", available_columns, key=f"{key_prefix}_date_col")
                
                with col2:
                    description_column = st.selectbox("Description Column", available_columns, key=f"{key_prefix}_desc_col")
                
                with col3:
                    amount_column = st.selectbox("Amount Column", available_columns, key=f"{key_prefix}_amount_col")
                
                with col4:
                    category_column = st.selectbox("Category Column (Optional)", available_columns, key=f"{key_prefix}_category_col")
                
                # Preview
                st.subheader("👀 Preview")
                st.dataframe(sample_df.head(), use_container_width=True)
                
            except Exception as e:
                st.error(f"Error reading CSV file: {str(e)}")
                return None
        
        # Submit button
        submitted = st.form_submit_button("📥 Import Data", type="primary")
        
        if submitted and uploaded_file is not None:
            try:
                # Read the full CSV
                df = pd.read_csv(uploaded_file, delimiter=delimiter, header=0 if has_header else None)
                
                # Validate required columns are mapped
                if not all([date_column, description_column, amount_column]):
                    st.error("Please map all required columns (Date, Description, Amount)")
                    return None
                
                # Create the transaction DataFrame
                transaction_data = {
                    'date': pd.to_datetime(df[date_column], format=date_format),
                    'description': df[description_column],
                    'amount': pd.to_numeric(df[amount_column]),
                    'category': df[category_column] if category_column else 'Imported',
                    'type': df[amount_column].apply(lambda x: 'Income' if float(x) > 0 else 'Expense')
                }
                
                imported_df = pd.DataFrame(transaction_data)
                
                st.success(f"Successfully imported {len(imported_df)} transactions!")
                st.dataframe(imported_df.head(), use_container_width=True)
                
                return imported_df
                
            except Exception as e:
                st.error(f"Error importing data: {str(e)}")
                return None
    
    return None

def create_export_form(
    data: pd.DataFrame,
    key_prefix: str = "export"
) -> None:
    """
    Create a form for exporting transaction data.
    
    Args:
        data: DataFrame containing transaction data
        key_prefix: Prefix for form element keys
    """
    if data.empty:
        st.info("No data available for export.")
        return
    
    st.subheader("📤 Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Export format
        export_format = st.selectbox(
            "Export Format",
            ["CSV", "Excel", "JSON"],
            key=f"{key_prefix}_format"
        )
        
        # Date range for export
        min_date = data['date'].min().date()
        max_date = data['date'].max().date()
        
        export_date_range = st.date_input(
            "Date Range to Export",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key=f"{key_prefix}_date_range"
        )
    
    with col2:
        # Columns to include
        available_columns = list(data.columns)
        selected_columns = st.multiselect(
            "Columns to Include",
            available_columns,
            default=available_columns,
            key=f"{key_prefix}_columns"
        )
        
        # Include summary
        include_summary = st.checkbox(
            "Include Summary Statistics",
            value=True,
            key=f"{key_prefix}_summary"
        )
    
    # Filter data for export
    if len(export_date_range) == 2:
        start_date, end_date = export_date_range
        export_data = data[
            (data['date'].dt.date >= start_date) & 
            (data['date'].dt.date <= end_date)
        ][selected_columns]
    else:
        export_data = data[selected_columns]
    
    # Show export preview
    st.subheader("📋 Export Preview")
    st.write(f"Rows to export: {len(export_data)}")
    st.dataframe(export_data.head(), use_container_width=True)
    
    # Generate download button
    if not export_data.empty:
        filename = f"transactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if export_format == "CSV":
            csv_data = export_data.to_csv(index=False)
            st.download_button(
                label="📄 Download CSV",
                data=csv_data,
                file_name=f"{filename}.csv",
                mime="text/csv"
            )
        
        elif export_format == "Excel":
            # Note: This requires openpyxl or xlsxwriter
            try:
                excel_buffer = pd.ExcelWriter(f"{filename}.xlsx", engine='openpyxl')
                export_data.to_excel(excel_buffer, index=False, sheet_name='Transactions')
                
                if include_summary:
                    # Add summary sheet
                    summary_data = {
                        'Metric': ['Total Income', 'Total Expenses', 'Net Amount', 'Transaction Count'],
                        'Value': [
                            export_data[export_data['amount'] > 0]['amount'].sum(),
                            export_data[export_data['amount'] < 0]['amount'].sum(),
                            export_data['amount'].sum(),
                            len(export_data)
                        ]
                    }
                    pd.DataFrame(summary_data).to_excel(excel_buffer, index=False, sheet_name='Summary')
                
                excel_buffer.close()
                
                with open(f"{filename}.xlsx", "rb") as f:
                    st.download_button(
                        label="📊 Download Excel",
                        data=f.read(),
                        file_name=f"{filename}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            except ImportError:
                st.warning("Excel export requires additional dependencies. Using CSV instead.")
                csv_data = export_data.to_csv(index=False)
                st.download_button(
                    label="📄 Download CSV",
                    data=csv_data,
                    file_name=f"{filename}.csv",
                    mime="text/csv"
                )
        
        elif export_format == "JSON":
            json_data = export_data.to_json(orient='records', date_format='iso')
            st.download_button(
                label="📋 Download JSON",
                data=json_data,
                file_name=f"{filename}.json",
                mime="application/json"
            )﻿ 
