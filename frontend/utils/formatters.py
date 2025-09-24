from datetime import datetime
from typing import Union

def format_currency(amount: Union[float, int], currency: str = "$") -> str:
    """Format amount as currency"""
    return f"{currency}{amount:,.2f}"

def format_date(date_string: str, format: str = "MMM DD, YYYY") -> str:
    """Format date string"""
    try:
        date_obj = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        if format == "MMM DD, YYYY":
            return date_obj.strftime("%b %d, %Y")
        elif format == "DD/MM/YYYY":
            return date_obj.strftime("%d/%m/%Y")
        elif format == "MM/DD/YYYY":
            return date_obj.strftime("%m/%d/%Y")
        else:
            return date_obj.strftime("%Y-%m-%d")
    except:
        return date_string[:10]

def format_percentage(value: float, decimals: int = 1) -> str:
    """Format value as percentage"""
    return f"{value:.{decimals}f}%"

def format_number(value: Union[float, int], decimals: int = 0) -> str:
    """Format number with thousand separators"""
    if decimals > 0:
        return f"{value:,.{decimals}f}"
    return f"{value:,.0f}"﻿ 
