import requests
from typing import Optional, Dict, List
import streamlit as st

class APIClient:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.headers = {}
        
        # Set auth header if token exists
        if 'token' in st.session_state:
            self.headers['Authorization'] = f"Bearer {st.session_state.token}"
    
    def login(self, username: str, password: str) -> Optional[str]:
        """Login user and return token"""
        try:
            response = requests.post(
                f"{self.base_url}/token",
                data={"username": username, "password": password}
            )
            if response.status_code == 200:
                return response.json()["access_token"]
            return None
        except:
            return None
    
    def register(self, email: str, username: str, password: str) -> Optional[Dict]:
        """Register new user"""
        try:
            response = requests.post(
                f"{self.base_url}/api/users/register",
                json={"email": email, "username": username, "password": password}
            )
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None
    
    def get_current_user(self) -> Optional[Dict]:
        """Get current user info"""
        try:
            response = requests.get(
                f"{self.base_url}/api/users/me",
                headers=self.headers
            )
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None
    
    def get_transactions(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """Get user transactions"""
        try:
            response = requests.get(
                f"{self.base_url}/api/transactions",
                headers=self.headers,
                params={"skip": skip, "limit": limit}
            )
            if response.status_code == 200:
                return response.json()
            return []
        except:
            return []
    
    def add_transaction(self, transaction: Dict) -> Optional[Dict]:
        """Add new transaction"""
        try:
            response = requests.post(
                f"{self.base_url}/api/transactions",
                json=transaction,
                headers=self.headers
            )
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None
    
        def delete_transaction(self, transaction_id: int) -> bool:
        """Delete transaction"""
        try:
            response = requests.delete(
                f"{self.base_url}/api/transactions/{transaction_id}",
                headers=self.headers
            )
            return response.status_code == 200
        except:
            return False
    
    def get_monthly_summary(self, month: str) -> Dict:
        """Get monthly summary"""
        try:
            response = requests.get(
                f"{self.base_url}/api/analytics/monthly-summary/{month}",
                headers=self.headers
            )
            if response.status_code == 200:
                return response.json()
            return {}
        except:
            return {}
    
    def get_category_breakdown(self, month: Optional[str] = None) -> List[Dict]:
        """Get category breakdown"""
        try:
            params = {"month": month} if month else {}
            response = requests.get(
                f"{self.base_url}/api/analytics/category-breakdown",
                headers=self.headers,
                params=params
            )
            if response.status_code == 200:
                return response.json()
            return []
        except:
            return []
    
    def get_budgets(self) -> List[Dict]:
        """Get user budgets"""
        try:
            response = requests.get(
                f"{self.base_url}/api/analytics/budgets",
                headers=self.headers
            )
            if response.status_code == 200:
                return response.json()
            return []
        except:
            return []
    
    def add_budget(self, budget: Dict) -> Optional[Dict]:
        """Add new budget"""
        try:
            response = requests.post(
                f"{self.base_url}/api/analytics/budgets",
                json=budget,
                headers=self.headers
            )
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None
    
    def get_categories(self) -> List[str]:
        """Get available categories"""
        return ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Other"]
