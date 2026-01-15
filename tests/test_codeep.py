"""Tests for Codeep AI SDK"""

import pytest
from unittest.mock import Mock, patch
from src.codeep import CodeepClient, CodeepLLM, Config
from src.codeep.tasks import TaskClient
from src.codeep.exceptions import (
    AuthenticationError,
    TaskError,
    APIError,
    NetworkError,
    ValidationError,
    TaskTimeoutError,
)


class TestCodeepClient:
    """Test CodeepClient functionality"""

    def setup_method(self):
        """Setup test fixtures"""
        self.client = CodeepClient()
        self.mock_response = Mock()
        self.mock_response.raise_for_status.return_value = None

    @patch('requests.Session.get')
    def test_health_check(self, mock_get):
        """Test health check endpoint"""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"status": "healthy", "service": "Codeep AI API"}
        mock_get.return_value = mock_response

        result = self.client.health_check()

        assert result["status"] == "healthy"
        assert result["service"] == "Codeep AI API"
        mock_get.assert_called_once()

    @patch('requests.Session.post')
    def test_register_success(self, mock_post):
        """Test successful user registration"""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "message": "User registered successfully",
            "user": {
                "id": 1,
                "username": "testuser",
                "email": "test@example.com",
                "api_key": "test_key",
                "daily_limit": 100,
                "created_at": "2023-12-01T00:00:00Z"
            }
        }
        mock_post.return_value = mock_response

        result = self.client.register("testuser", "test@example.com", "password")

        assert result["message"] == "User registered successfully"
        assert result["user"]["username"] == "testuser"

    @patch('requests.Session.post')
    def test_login_success(self, mock_post):
        """Test successful login"""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "access_token": "test_token",
            "user": {
                "id": 1,
                "username": "testuser",
                "email": "test@example.com",
                "api_key": "test_key",
                "daily_limit": 100,
                "created_at": "2023-12-01T00:00:00Z"
            }
        }
        mock_post.return_value = mock_response

        result = self.client.login("testuser", "password")

        assert result["access_token"] == "test_token"
        # Check that Authorization header was set
        assert self.client.auth.session.headers["Authorization"] == "Bearer test_token"

    def test_set_token(self):
        """Test manual token setting"""
        token = "manual_token"
        self.client.set_token(token)

        assert self.client.auth.session.headers["Authorization"] == f"Bearer {token}"


class TestExceptions:
    """Test custom exceptions"""

    def test_codeep_exception_creation(self):
        """Test base CodeepException"""
        exc = AuthenticationError("Test message", 401)
        assert str(exc) == "Test message"
        assert exc.status_code == 401

    def test_task_error_creation(self):
        """Test TaskError"""
        exc = TaskError("Task failed", 500)
        assert str(exc) == "Task failed"
        assert exc.status_code == 500

    def test_api_error_with_details(self):
        """Test APIError with error details"""
        details = {"field": "required"}
        exc = APIError("Validation failed", 400, details)
        assert str(exc) == "Validation failed"
        assert exc.status_code == 400
        assert exc.error_details == details


class TestConfig:
    """Test configuration functionality"""

    def test_config_base_url(self):
        """Test base URL configuration"""
        original_url = Config.API_BASE_URL

        Config.set_base_url("https://test.com/v1")
        assert Config.get_base_url() == "https://test.com/v1"

        # Reset
        Config.API_BASE_URL = original_url

    def test_config_environment(self):
        """Test environment configuration"""
        original_env = Config.ENVIRONMENT

        Config.set_environment("development")
        assert Config.ENVIRONMENT == "development"
        assert Config.get_base_url() == "http://localhost:5001"

        Config.set_environment("production")
        assert Config.ENVIRONMENT == "production"
        assert Config.get_base_url() == "https://api.codeep.cc/v1"

        # Reset
        Config.ENVIRONMENT = original_env


class TestCodeepLLM:
    """Test LangChain LLM integration"""

    def setup_method(self):
        """Setup test fixtures"""
        self.mock_client = Mock(spec=TaskClient)
        self.llm = CodeepLLM(client=self.mock_client)

    def test_llm_initialization(self):
        """Test LLM initialization"""
        assert self.llm.client == self.mock_client
        assert self.llm.model_name == "codeep-ai"
        assert self.llm.timeout == 300
        assert self.llm.poll_interval == 5

    def test_llm_type(self):
        """Test LLM type property"""
        assert self.llm._llm_type == "codeep_ai"

    def test_identifying_params(self):
        """Test identifying parameters"""
        params = self.llm._identifying_params
        assert params["model_name"] == "codeep-ai"
        assert params["timeout"] == 300
        assert params["poll_interval"] == 5

    def test_call_success(self):
        """Test successful LLM call"""
        # Mock task creation and completion
        mock_task = Mock()
        mock_task.task_id = "test_task_id"
        self.mock_client.create_task.return_value = mock_task

        mock_completed_task = Mock()
        mock_completed_task.status = "completed"
        mock_completed_task.result = "Test response"
        self.mock_client.wait_for_completion.return_value = mock_completed_task

        result = self.llm._call("Test prompt")

        assert result == "Test response"
        self.mock_client.create_task.assert_called_once_with(prompt="Test prompt", toolset=None)

    def test_call_task_failed(self):
        """Test LLM call with task failure"""
        # Mock task creation and completion
        mock_task = Mock()
        mock_task.task_id = "test_task_id"
        self.mock_client.create_task.return_value = mock_task

        mock_completed_task = Mock()
        mock_completed_task.status = "failed"
        mock_completed_task.error_message = "Task error"
        self.mock_client.wait_for_completion.return_value = mock_completed_task

        with pytest.raises(TaskError):
            self.llm._call("Test prompt")


if __name__ == "__main__":
    pytest.main([__file__])