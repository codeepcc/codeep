"""LangChain compatible LLM implementation for Codeep AI"""

from typing import Any, Dict, Iterator, List, Optional, Union
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from langchain_core.outputs import Generation, GenerationChunk, LLMResult
from pydantic import Field, field_validator

from .tasks import TaskClient
from .exceptions import TaskError


class CodeepLLM(LLM):
    """LangChain compatible LLM for Codeep AI"""

    client: Union[TaskClient, Any] = Field(...)
    model_name: str = Field(default="codeep-ai")
    toolset: Optional[List[str]] = Field(default=None)
    timeout: int = Field(default=300)
    poll_interval: int = Field(default=5)

    @field_validator("client", mode="before")
    @classmethod
    def validate_environment(cls, v):
        """Validate that task client is provided"""
        if v is None:
            raise ValueError("Must provide task client")
        return v

    @property
    def _llm_type(self) -> str:
        """Return the type of LLM"""
        return "codeep_ai"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Call the Codeep AI API"""
        # Create task
        task = self.client.create_task(prompt=prompt, toolset=self.toolset)

        # Wait for completion
        completed_task = self.client.wait_for_completion(
            task.task_id,
            timeout=self.timeout,
            poll_interval=self.poll_interval
        )

        if completed_task.status == "failed":
            error_msg = completed_task.error_message or "Task failed"
            raise TaskError(f"Codeep AI task failed: {error_msg}")

        if completed_task.result is None:
            raise TaskError("Task completed but no result returned")

        # Handle stop sequences
        if stop:
            for stop_seq in stop:
                if stop_seq in completed_task.result:
                    completed_task.result = completed_task.result.split(stop_seq)[0]
                    break

        return completed_task.result

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Get the identifying parameters"""
        return {
            "model_name": self.model_name,
            "toolset": self.toolset,
            "timeout": self.timeout,
            "poll_interval": self.poll_interval,
        }

    def _generate(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> LLMResult:
        """Generate completions for multiple prompts"""
        generations = []
        for prompt in prompts:
            try:
                text = self._call(prompt, stop=stop, run_manager=run_manager, **kwargs)
                generations.append([Generation(text=text)])
            except Exception as e:
                # For multiple prompts, we continue with empty generation on error
                generations.append([Generation(text="")])

        return LLMResult(generations=generations)

    def _stream(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[GenerationChunk]:
        """Stream the response (not supported by Codeep AI API)"""
        # Codeep AI doesn't support streaming, so we simulate it by returning the full result
        try:
            text = self._call(prompt, stop=stop, run_manager=run_manager, **kwargs)
            yield GenerationChunk(text=text)
        except Exception as e:
            yield GenerationChunk(text="")