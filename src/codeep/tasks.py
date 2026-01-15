"""Task management module for Codeep AI API"""

import time
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
import requests
from .config import Config


class Task(BaseModel):
    task_id: str
    user_id: int
    prompt: str
    toolset: Optional[List[str]] = None
    status: str
    result: Optional[str] = None
    error_message: Optional[str] = None
    created_at: str
    updated_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


class TaskClient:
    """Client for task management endpoints"""

    def __init__(self, base_url: Optional[str] = None, session: Optional[requests.Session] = None):
        self.base_url = (base_url or Config.get_base_url()).rstrip("/")
        self.session = session or requests.Session()

    def create_task(self, prompt: str, toolset: Optional[List[str]] = None) -> Task:
        """Create a new task"""
        url = f"{self.base_url}/tasks/tasks"
        payload = {"prompt": prompt}
        if toolset:
            payload["toolset"] = toolset

        response = self.session.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        return Task(**data["task"])

    def get_user_tasks(self) -> List[Task]:
        """Get all tasks for the authenticated user"""
        url = f"{self.base_url}/tasks/tasks"
        response = self.session.get(url)
        response.raise_for_status()
        data = response.json()
        return [Task(**task) for task in data["tasks"]]

    def get_task(self, task_id: str) -> Task:
        """Get specific task details"""
        url = f"{self.base_url}/tasks/tasks/{task_id}"
        response = self.session.get(url)
        response.raise_for_status()
        data = response.json()
        return Task(**data["task"])

    def update_task(self, task_id: str, **kwargs) -> Task:
        """Update task information"""
        url = f"{self.base_url}/tasks/tasks/{task_id}"
        response = self.session.put(url, json=kwargs)
        response.raise_for_status()
        data = response.json()
        return Task(**data["task"])

    def delete_task(self, task_id: str) -> Dict:
        """Delete a task"""
        url = f"{self.base_url}/tasks/tasks/{task_id}"
        response = self.session.delete(url)
        response.raise_for_status()
        return response.json()

    def get_task_results(self, task_id: str) -> Dict:
        """Get detailed results for a completed task"""
        url = f"{self.base_url}/tasks/tasks/{task_id}/results"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def wait_for_completion(self, task_id: str, timeout: int = 300, poll_interval: int = 5) -> Task:
        """Wait for task completion with polling"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            task = self.get_task(task_id)
            if task.status in ["completed", "failed"]:
                return task
            time.sleep(poll_interval)
        raise TimeoutError(f"Task {task_id} did not complete within {timeout} seconds")

    def get_queue_status(self) -> Dict:
        """Get current queue statistics"""
        url = f"{self.base_url}/tasks/queue/status"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()