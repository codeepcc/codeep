"""Main client for Codeep AI API"""

from typing import Dict, List, Optional
from .auth import AuthClient, User
from .tasks import TaskClient, Task
from .llm import CodeepLLM
from .config import Config


class CodeepClient:
    """Main client for Codeep AI API"""

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or Config.get_base_url()
        self.auth = AuthClient(self.base_url)
        self.tasks = TaskClient(self.base_url, session=self.auth.session)
        self._llm: Optional[CodeepLLM] = None

    def login(self, username: str, password: str) -> Dict:
        """Login and get access token"""
        return self.auth.login(username, password)

    def register(self, username: str, email: str, password: str) -> Dict:
        """Register a new user"""
        return self.auth.register(username, email, password)

    def set_token(self, token: str):
        """Manually set authentication token"""
        self.auth.set_token(token)

    def get_current_user(self) -> User:
        """Get current user information"""
        return self.auth.get_current_user()

    def get_quota(self) -> Dict:
        """Get user quota information"""
        return self.auth.get_quota()

    def validate_quota(self) -> Dict:
        """Validate if user has remaining quota"""
        return self.auth.validate_quota()

    def create_task(self, prompt: str, toolset: Optional[List[str]] = None) -> Task:
        """Create a new task"""
        return self.tasks.create_task(prompt, toolset)

    def get_user_tasks(self) -> List[Task]:
        """Get all tasks for the authenticated user"""
        return self.tasks.get_user_tasks()

    def get_task(self, task_id: str) -> Task:
        """Get specific task details"""
        return self.tasks.get_task(task_id)

    def wait_for_completion(self, task_id: str, timeout: int = 300, poll_interval: int = 5) -> Task:
        """Wait for task completion with polling"""
        return self.tasks.wait_for_completion(task_id, timeout, poll_interval)

    def get_task_results(self, task_id: str) -> Dict:
        """Get detailed results for a completed task"""
        return self.tasks.get_task_results(task_id)

    def get_queue_status(self) -> Dict:
        """Get current queue statistics"""
        return self.tasks.get_queue_status()

    @property
    def llm(self) -> CodeepLLM:
        """Get LangChain compatible LLM instance"""
        if self._llm is None:
            self._llm = CodeepLLM(client=self.tasks)
        return self._llm

    def get_dashboard_stats(self) -> Dict:
        """Get dashboard statistics (requires auth)"""
        url = f"{self.base_url}/dashboard/stats"
        response = self.auth.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_task_history(
        self,
        page: int = 1,
        per_page: int = 20,
        status: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> Dict:
        """Get paginated task history"""
        url = f"{self.base_url}/dashboard/tasks/history"
        params = {
            "page": page,
            "per_page": per_page
        }
        if status:
            params["status"] = status
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        response = self.auth.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_usage_analytics(self, days: int = 30) -> Dict:
        """Get usage analytics"""
        url = f"{self.base_url}/dashboard/usage"
        params = {"days": days}
        response = self.auth.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def health_check(self) -> Dict:
        """Check API health status"""
        url = f"{self.base_url}/health"
        response = self.auth.session.get(url)
        response.raise_for_status()
        return response.json()