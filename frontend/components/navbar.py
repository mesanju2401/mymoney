import streamlit as st
from utils.session_manager import SessionManager

def render_navbar():
    """Render the navigation bar"""
    session_manager = SessionManager()
    
    with st.sidebar:
        st.markdown("# MyMoney 💰")
        st.markdown(f"Welcome, **{session_manager.get_username()}**!")
        st.markdown("---")
        
        # Navigation links
        st.page_link("app.py", label="🏠 Dashboard", icon="🏠")
        st.page_link("pages/1_Transactions.py", label="💸 Transactions", icon="💸")
        st.page_link("pages/2_Analytics.py", label="📊 Analytics", icon="📊")
        st.page_link("pages/3_Budget.py", label="💰 Budget", icon="💰")
        st.page_link("pages/4_Settings.py", label="⚙️ Settings", icon="⚙️")
        
        st.markdown("---")
        
        # Quick stats
        st.markdown("### Quick Stats")
        st.metric("This Month", "$2,450", "+12%")
        st.metric("Saved", "$450", "+5%")
