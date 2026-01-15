"""Authentication module for Codeep AI API"""

import requests
from typing import Dict, Optional
from pydantic import BaseModel
from .config import Config
from .exceptions import (
    AuthenticationError,
    AuthorizationError,
    QuotaExceededError,
    APIError,
    NetworkError,
    ValidationError,
)


class User(BaseModel):
    id: int
    username: str
    email: str
    api_key: str
    daily_limit: int
    created_at: str


class AuthClient:
    """Client for authentication endpoints"""

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = (base_url or Config.get_base_url()).rstrip("/")
        self.session = requests.Session()

    def register(self, username: str, email: str, password: str) -> Dict:
        """Register a new user"""
        url = f"{self.base_url}/auth/register"
        payload = {
            "username": username,
            "email": email,
            "password": password
        }
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def login(self, username: str, password: str) -> Dict:
        """Login and get access token"""
        url = f"{self.base_url}/auth/login"
        payload = {
            "username": username,
            "password": password
        }
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        # Store token for future requests
        self.session.headers.update({"Authorization": f"Bearer {data['access_token']}"})
        return data

    def get_current_user(self) -> User:
        """Get current user information"""
        url = f"{self.base_url}/auth/me"
        response = self.session.get(url)
        response.raise_for_status()
        data = response.json()
        return User(**data["user"])

    def get_quota(self) -> Dict:
        """Get user quota information"""
        url = f"{self.base_url}/auth/quota"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def validate_quota(self) -> Dict:
        """Validate if user has remaining quota"""
        url = f"{self.base_url}/auth/quota/validate"
        response = self.session.get(url)
        if response.status_code == 429:
            return response.json()
        response.raise_for_status()
        return response.json()

    def set_token(self, token: str):
        """Manually set authentication token"""
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def clear_token(self):
        """Clear authentication token"""
        self.session.headers.pop("Authorization", None)