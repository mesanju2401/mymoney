"""
Navigation components for the Personal Finance Tracker application.

This module contains functions to create navigation elements like sidebars,
quick action menus, and navigation bars.
"""

import streamlit as st
from typing import Dict, List, Optional, Callable

def create_sidebar_navigation(
    current_page: str = "Dashboard",
    show_user_info: bool = True
) -> str:
    """
    Create a sidebar navigation menu.
    
    Args:
        current_page: Current active page name
        show_user_info: Whether to show user information section
        
    Returns:
        Selected page name
    """
    with st.sidebar:
        # App header
        st.markdown(
            """
            <div style="text-align: center; padding: 1rem 0;">
                <h2 style="color: #1f77b4; margin: 0;">💰 Finance Tracker</h2>
                <p style="color: #666; margin: 0; font-size: 0.9rem;">Personal Finance Management</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("---")
        
        # User info section
        if show_user_info:
            st.markdown("### 👤 User Profile")
            
            # This would typically come from a user authentication system
            user_name = st.session_state.get('user_name', 'Guest User')
            user_email = st.session_state.get('user_email', 'guest@example.com')
            
            st.write(f"**Name:** {user_name}")
            st.write(f"**Email:** {user_email}")
            
            if st.button("⚙️ Profile Settings", key="profile_settings"):
                st.switch_page("pages/4_Settings.py")
            
            st.markdown("---")
        
        # Navigation menu
        st.markdown("### 🧭 Navigation")
        
        pages = {
            "🏠 Dashboard": "app.py",
            "💳 Transactions": "pages/1_Transactions.py",
            "📊 Analytics": "pages/2_Analytics.py",
            "💼 Budget": "pages/3_Budget.py",
            "⚙️ Settings": "pages/4_Settings.py"
        }
        
        selected_page = None
        
        for page_name, page_file in pages.items():
            # Highlight current page
            if current_page.lower() in page_name.lower():
                st.markdown(
                    f"""
                    <div style="
                        background: linear-gradient(90deg, #667eea, #764ba2);
                        color: white;
                        padding: 0.5rem;
                        border-radius: 5px;
                        margin: 0.2rem 0;
                        font-weight: bold;
                    ">
                        {page_name}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                if st.button(page_name, key=f"nav_{page_name}", use_container_width=True):
                    selected_page = page_file
        
        st.markdown("---")
        
        return selected_page

def create_quick_actions(
    show_balance: bool = True,
    balance_data: Optional[Dict] = None
) -> Optional[str]:
    """
    Create quick action buttons in the sidebar.
    
    Args:
        show_balance: Whether to show balance summary
        balance_data: Dictionary containing balance information
        
    Returns:
        Action identifier if button was clicked
    """
    with st.sidebar:
        st.markdown("### ⚡ Quick Actions")
        
        action_clicked = None
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("➕ Add Income", key="quick_add_income", use_container_width=True):
                action_clicked = "add_income"
            
            if st.button("📊 View Reports", key="quick_view_reports", use_container_width=True):
                action_clicked = "view_reports"
        
        with col2:
            if st.button("➖ Add Expense", key="quick_add_expense", use_container_width=True):
                action_clicked = "add_expense"
            
            if st.button("💼 Set Budget", key="quick_set_budget", use_container_width=True):
                action_clicked = "set_budget"
        
        # Balance summary
        if show_balance and balance_data:
            st.markdown("---")
            st.markdown("### 💰 Quick Balance")
            
            total_income = balance_data.get('income', 0)
            total_expenses = balance_data.get('expenses', 0)
            net_balance = total_income - abs(total_expenses)
            
            # Income
            st.markdown(
                f"""
                <div style="
                    background: linear-gradient(90deg, #28a745, #20c997);
                    color: white;
                    padding: 0.8rem;
                    border-radius: 8px;
                    margin: 0.5rem 0;
                    text-align: center;
                ">
                    <div style="font-size: 0.8rem; opacity: 0.9;">Total Income</div>
                    <div style="font-size: 1.2rem; font-weight: bold;">₹{total_income:,.0f}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Expenses
            st.markdown(
                f"""
                <div style="
                    background: linear-gradient(90deg, #dc3545, #fd7e14);
                    color: white;
                    padding: 0.8rem;
                    border-radius: 8px;
                    margin: 0.5rem 0;
                    text-align: center;
                ">
                    <div style="font-size: 0.8rem; opacity: 0.9;">Total Expenses</div>
                    <div style="font-size: 1.2rem; font-weight: bold;">₹{abs(total_expenses):,.0f}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Net Balance
            balance_color = "#28a745" if net_balance >= 0 else "#dc3545"
            st.markdown(
                f"""
                <div style="
                    background: {balance_color};
                    color: white;
                    padding: 0.8rem;
                    border-radius: 8px;
                    margin: 0.5rem 0;
                    text-align: center;
                    border: 2px solid rgba(255,255,255,0.3);
                ">
                    <div style="font-size: 0.8rem; opacity: 0.9;">Net Balance</div>
                    <div style="font-size: 1.3rem; font-weight: bold;">₹{net_balance:,.0f}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown("---")
        
        return action_clicked

def create_top_navbar(
    title: str = "Personal Finance Tracker",
    show_breadcrumb: bool = True,
    breadcrumb_items: Optional[List[str]] = None
) -> None:
    """
    Create a top navigation bar.
    
    Args:
        title: Main title for the navbar
        show_breadcrumb: Whether to show breadcrumb navigation
        breadcrumb_items: List of breadcrumb items
    """
    # Main navbar
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h1 style="margin: 0; font-size: 1.8rem;">{title}</h1>
                    <div style="font-size: 0.9rem; opacity: 0.9; margin-top: 0.2rem;">
                        Manage your finances with ease
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 0.8rem; opacity: 0.8;">Today</div>
                    <div style="font-size: 1rem; font-weight: bold;">
                        {st.session_state.get('current_date', 'Sept 25, 2024')}
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Breadcrumb
    if show_breadcrumb and breadcrumb_items:
        breadcrumb_html = " → ".join([f"<span>{item}</span>" for item in breadcrumb_items])
        st.markdown(
            f"""
            <div style="
                background: #f8f9fa;
                padding: 0.5rem 1rem;
                border-radius: 5px;
                margin-bottom: 1rem;
                border-left: 4px solid #667eea;
            ">
                <div style="color: #6c757d; font-size: 0.9rem;">
                    {breadcrumb_html}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

def create_footer() -> None:
    """Create a footer for the application."""
    st.markdown(
        """
        <div style="
            margin-top: 3rem;
            padding: 2rem 0;
            border-top: 1px solid #dee2e6;
            text-align: center;
            color: #6c757d;
        ">
            <div style="margin-bottom: 1rem;">
                <strong>Personal Finance Tracker</strong> - Take control of your financial future
            </div>
            <div style="font-size: 0.9rem;">
                💡 Track expenses • 📊 Analyze spending • 💼 Set budgets • 🎯 Achieve goals
            </div>
            <div style="margin-top: 1rem; font-size: 0.8rem;">
                Made with ❤️ using Streamlit • Version 1.0.0
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def create_notification_bar(
    notifications: List[Dict],
    show_count: bool = True
) -> None:
    """
    Create a notification bar showing alerts and messages.
    
    Args:
        notifications: List of notification dictionaries
        show_count: Whether to show notification count
    """
    if not notifications:
        return
    
    # Notification count badge
    if show_count:
        count = len(notifications)
        st.markdown(
            f"""
            <div style="
                display: inline-block;
                background: #dc3545;
                color: white;
                padding: 0.2rem 0.6rem;
                border-radius: 15px;
                font-size: 0.8rem;
                font-weight: bold;
                margin-bottom: 1rem;
            ">
                🔔 {count} notification{'s' if count != 1 else ''}
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Show notifications
    for notification in notifications[:5]:  # Show max 5 notifications
        notification_type = notification.get('type', 'info')
        title = notification.get('title', 'Notification')
        message = notification.get('message', '')
        
        # Color scheme based on type
        colors = {
            'info': {'bg': '#d1ecf1', 'border': '#bee5eb', 'text': '#0c5460'},
            'success': {'bg': '#d4edda', 'border': '#c3e6cb', 'text': '#155724'},
            'warning': {'bg': '#fff3cd', 'border': '#ffeaa7', 'text': '#856404'},
            'error': {'bg': '#f8d7da', 'border': '#f5c6cb', 'text': '#721c24'}
        }
        
        color_scheme = colors.get(notification_type, colors['info'])
        
        # Icons for different notification types
        icons = {
            'info': 'ℹ️',
            'success': '✅',
            'warning': '⚠️',
            'error': '❌'
        }
        
        icon = icons.get(notification_type, '🔔')
        
        st.markdown(
            f"""
            <div style="
                background: {color_scheme['bg']};
                color: {color_scheme['text']};
                padding: 1rem;
                border-radius: 8px;
                border: 1px solid {color_scheme['border']};
                margin: 0.5rem 0;
                border-left: 4px solid {color_scheme['border']};
            ">
                <div style="font-weight: 600; margin-bottom: 0.5rem;">
                    {icon} {title}
                </div>
                <div style="font-size: 0.9rem;">{message}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

def create_settings_menu() -> Optional[str]:
    """
    Create a settings menu with various configuration options.
    
    Returns:
        Selected setting action if any
    """
    st.markdown("### ⚙️ Settings")
    
    settings_action = None
    
    # Theme settings
    with st.expander("🎨 Theme Settings", expanded=False):
        theme = st.selectbox(
            "Choose Theme",
            ["Light", "Dark", "Auto"],
            key="theme_setting"
        )
        
        color_scheme = st.selectbox(
            "Color Scheme",
            ["Blue", "Green", "Purple", "Orange"],
            key="color_scheme_setting"
        )
        
        if st.button("Apply Theme", key="apply_theme"):
            settings_action = "apply_theme"
            st.success("Theme settings applied!")
    
    # Currency settings
    with st.expander("💱 Currency Settings", expanded=False):
        currency = st.selectbox(
            "Default Currency",
            ["INR (₹)", "USD ($)", "EUR (€)", "GBP (£)"],
            key="currency_setting"
        )
        
        decimal_places = st.slider(
            "Decimal Places",
            min_value=0,
            max_value=4,
            value=2,
            key="decimal_places_setting"
        )
        
        thousands_separator = st.checkbox(
            "Use Thousands Separator",
            value=True,
            key="thousands_separator_setting"
        )
        
        if st.button("Save Currency Settings", key="save_currency"):
            settings_action = "save_currency"
            st.success("Currency settings saved!")
    
    # Notification settings
    with st.expander("🔔 Notification Settings", expanded=False):
        email_notifications = st.checkbox(
            "Email Notifications",
            value=True,
            key="email_notifications_setting"
        )
        
        budget_alerts = st.checkbox(
            "Budget Alert Notifications",
            value=True,
            key="budget_alerts_setting"
        )
        
        weekly_summary = st.checkbox(
            "Weekly Summary Email",
            value=False,
            key="weekly_summary_setting"
        )
        
        monthly_report = st.checkbox(
            "Monthly Report Email",
            value=True,
            key="monthly_report_setting"
        )
        
        if st.button("Save Notification Settings", key="save_notifications"):
            settings_action = "save_notifications"
            st.success("Notification settings saved!")
    
    # Data management
    with st.expander("📊 Data Management", expanded=False):
        st.markdown("**Export Data**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 Export All Data", key="export_all_data"):
                settings_action = "export_all"
            
            if st.button("📊 Generate Report", key="generate_report"):
                settings_action = "generate_report"
        
        with col2:
            if st.button("🗄️ Backup Data", key="backup_data"):
                settings_action = "backup_data"
            
            if st.button("📥 Import Data", key="import_data"):
                settings_action = "import_data"
        
        st.markdown("---")
        st.markdown("**⚠️ Danger Zone**")
        
        if st.button("🗑️ Clear All Data", key="clear_all_data", type="secondary"):
            settings_action = "clear_all_data"
            st.warning("This action cannot be undone!")
    
    # Account settings
    with st.expander("👤 Account Settings", expanded=False):
        new_name = st.text_input(
            "Display Name",
            value=st.session_state.get('user_name', 'Guest User'),
            key="display_name_setting"
        )
        
        new_email = st.text_input(
            "Email Address",
            value=st.session_state.get('user_email', 'guest@example.com'),
            key="email_address_setting"
        )
        
        timezone = st.selectbox(
            "Timezone",
            ["Asia/Kolkata", "UTC", "America/New_York", "Europe/London"],
            key="timezone_setting"
        )
        
        if st.button("Update Profile", key="update_profile"):
            settings_action = "update_profile"
            st.session_state['user_name'] = new_name
            st.session_state['user_email'] = new_email
            st.success("Profile updated successfully!")
    
    return settings_action

def create_mobile_nav() -> None:
    """
    Create a mobile-friendly navigation menu.
    """
    # This creates a horizontal navigation for mobile devices
    st.markdown(
        """
        <style>
        .mobile-nav {
            display: flex;
            justify-content: space-around;
            background: linear-gradient(90deg, #667eea, #764ba2);
            padding: 0.5rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .mobile-nav-item {
            flex: 1;
            text-align: center;
            color: white;
            text-decoration: none;
            padding: 0.5rem;
            border-radius: 5px;
            font-size: 0.8rem;
        }
        
        .mobile-nav-item:hover {
            background: rgba(255, 255, 255, 0.1);
        }
        
        .mobile-nav-item.active {
            background: rgba(255, 255, 255, 0.2);
            font-weight: bold;
        }
        
        @media (min-width: 768px) {
            .mobile-nav {
                display: none;
            }
        }
        </style>
        
        <div class="mobile-nav">
            <div class="mobile-nav-item">🏠<br>Dashboard</div>
            <div class="mobile-nav-item">💳<br>Transactions</div>
            <div class="mobile-nav-item">📊<br>Analytics</div>
            <div class="mobile-nav-item">💼<br>Budget</div>
            <div class="mobile-nav-item">⚙️<br>Settings</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def create_help_section() -> None:
    """Create a help section with tips and shortcuts."""
    with st.sidebar:
        st.markdown("---")
        st.markdown("### ❓ Help & Tips")
        
        with st.expander("💡 Quick Tips", expanded=False):
            st.markdown("""
            **Getting Started:**
            - Add your first transaction using the form
            - Set up budgets to track spending
            - View analytics for insights
            
            **Shortcuts:**
            - Use quick action buttons for common tasks
            - Filter data using date ranges
            - Export data for external analysis
            
            **Tips:**
            - Categorize transactions for better insights
            - Set realistic budget limits
            - Review reports regularly
            """)
        
        with st.expander("🔧 Troubleshooting", expanded=False):
            st.markdown("""
            **Common Issues:**
            
            **Data not showing?**
            - Check your date filters
            - Ensure transactions are properly categorized
            
            **Charts not loading?**
            - Refresh the page
            - Check if you have sufficient data
            
            **Import issues?**
            - Verify CSV format matches requirements
            - Check date formats are consistent
            """)
        
        with st.expander("📞 Support", expanded=False):
            st.markdown("""
            **Need Help?**
            
            📧 Email: support@financetracker.com
            💬 Live Chat: Available 9 AM - 6 PM
            📚 Documentation: [View Guides]
            🐛 Report Bug: [Submit Issue]
            
            **Version:** 1.0.0
            **Last Updated:** Sept 25, 2024
            """)

def create_stats_summary() -> None:
    """Create a quick stats summary in the sidebar."""
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 📈 Quick Stats")
        
        # Get transaction data from session state
        if 'transactions' in st.session_state and not st.session_state.transactions.empty:
            df = st.session_state.transactions
            
            # Calculate stats
            total_transactions = len(df)
            this_month = df[df['date'].dt.month == pd.Timestamp.now().month]
            monthly_transactions = len(this_month)
            
            avg_transaction = df['amount'].abs().mean()
            most_common_category = df['category'].mode().iloc[0] if not df['category'].mode().empty else 'N/A'
            
            # Display stats
            st.metric("Total Transactions", total_transactions)
            st.metric("This Month", monthly_transactions)
            st.metric("Avg Transaction", f"₹{avg_transaction:,.0f}")
            
            st.markdown(f"**Top Category:** {most_common_category}")
            
            # Recent activity indicator
            recent_transactions = df[df['date'] >= pd.Timestamp.now() - pd.Timedelta(days=7)]
            if len(recent_transactions) > 0:
                st.success(f"✅ {len(recent_transactions)} transactions this week")
            else:
                st.info("ℹ️ No recent activity")
        
        else:
            st.info("📊 Add transactions to see stats")

def create_breadcrumb(items: List[str]) -> None:
    """
    Create a breadcrumb navigation.
    
    Args:
        items: List of breadcrumb items
    """
    if not items:
        return
    
    breadcrumb_items = []
    for i, item in enumerate(items):
        if i == len(items) - 1:  # Last item (current page)
            breadcrumb_items.append(f'<strong style="color: #495057;">{item}</strong>')
        else:
            breadcrumb_items.append(f'<span style="color: #6c757d;">{item}</span>')
    
    breadcrumb_html = ' <span style="color: #6c757d;">→</span> '.join(breadcrumb_items)
    
    st.markdown(
        f"""
        <div style="
            background: #f8f9fa;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            border-left: 4px solid #007bff;
            margin-bottom: 1.5rem;
            font-size: 0.9rem;
        ">
            🏠 {breadcrumb_html}
        </div>
        """,
        unsafe_allow_html=True
    )
