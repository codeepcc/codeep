"""Custom exceptions for Codeep AI SDK"""

from typing import Optional


class CodeepException(Exception):
    """Base exception for Codeep AI SDK"""

    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class AuthenticationError(CodeepException):
    """Raised when authentication fails"""
    pass


class AuthorizationError(CodeepException):
    """Raised when authorization fails (insufficient permissions)"""
    pass


class QuotaExceededError(CodeepException):
    """Raised when user quota is exceeded"""
    pass


class TaskError(CodeepException):
    """Raised when task execution fails"""
    pass


class TaskTimeoutError(TaskError):
    """Raised when task times out"""
    pass


class APIError(CodeepException):
    """Raised when API returns an error response"""

    def __init__(self, message: str, status_code: int, error_details: Optional[dict] = None):
        super().__init__(message, status_code)
        self.error_details = error_details


class NetworkError(CodeepException):
    """Raised when network-related errors occur"""
    pass


class ValidationError(CodeepException):
    """Raised when input validation fails"""
    pass