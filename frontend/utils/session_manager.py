import streamlit as st
from typing import Optional

class SessionManager:
    """Manage user session and authentication state"""
    
    def __init__(self):
        # Initialize session state
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'username' not in st.session_state:
            st.session_state.username = None
        if 'token' not in st.session_state:
            st.session_state.token = None
    
    def login(self, username: str, token: str):
        """Login user"""
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.token = token
    
    def logout(self):
        """Logout user"""
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.token = None
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return st.session_state.authenticated
    
    def get_username(self) -> Optional[str]:
        """Get current username"""
        return st.session_state.username
    
    def get_token(self) -> Optional[str]:
        """Get current token"""
        return st.session_state.token﻿ 
