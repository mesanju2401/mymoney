"""
Components package for the Personal Finance Tracker application.

This package contains reusable UI components for the Streamlit application.
"""

# Import all component modules to make them available when importing the package
try:
    from .cards import *
    from .charts import *
    from .forms import *
    from .navbar import *
except ImportError as e:
    # Handle import errors gracefully during development
    import warnings
    warnings.warn(f"Could not import some components: {e}")

# Package metadata
__version__ = "1.0.0"
__author__ = "Finance Tracker Team"

# Available components list
__all__ = [
    # From cards.py
    'create_metric_card',
    'create_summary_card',
    'create_info_card',
    
    # From charts.py
    'create_expense_pie_chart',
    'create_income_vs_expense_chart',
    'create_monthly_trend_chart',
    'create_category_bar_chart',
    
    # From forms.py
    'create_transaction_form',
    'create_budget_form',
    'create_filter_form',
    
    # From navbar.py
    'create_sidebar_navigation',
    'create_quick_actions',
]

def get_component_info():
    """
    Returns information about available components in this package.
    
    Returns:
        dict: Dictionary containing component information
    """
    return {
        "package_version": __version__,
        "available_components": __all__,
        "modules": [
            "cards - Reusable card components for displaying metrics and information",
            "charts - Chart components using Plotly for data visualization", 
            "forms - Form components for user input and data collection",
            "navbar - Navigation components for sidebar and menus"
        ]
    }

def init_components():
    """
    Initialize components package.
    This function can be called to set up any required configurations.
    """
    # Any initialization code can go here
    # For now, we'll just return a success message
    return "Components package initialized successfully"
