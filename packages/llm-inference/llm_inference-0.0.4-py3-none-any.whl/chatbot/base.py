import logging
from typing import Any, List, Optional

import requests
from langchain.llms.base import LLM
from pydantic import BaseModel

from llm_inference import LLMInference

logger = logging.getLogger(__name__)


class DummyLLM(LLM, BaseModel):
    def _call(self, prompt: str, stop: Optional[list[str]] = None) -> str:
        return f"Bot: {prompt}"

    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "Dummy LLM"


class LLaMALLM(LLM, BaseModel):
    checkpoint_dir: str = ""
    model: Any = None

    def _call(self, prompt: str, stop: Optional[list[str]] = None) -> str:
        if not self.model:
            self.model = LLMInference(
                checkpoint_dir=self.checkpoint_dir,
                precision="bf16-mixed",
            )

        return self.model(prompt)

    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "Lit-GPT LLM"


class ServerLLM(LLM, BaseModel):
    url: str = ""

    def _call(self, prompt: str, stop: Optional[list[str]] = None) -> str:
        """Run the LLM on the given prompt and input."""
        if self.url == "":
            raise Exception("Server URL not set!")

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        assert isinstance(prompt, str)
        json_data = {"prompt": prompt}
        response = requests.post(
            url=self.url + "/predict", headers=headers, json=json_data
        )
        logger.error(response.raise_for_status())
        return response.json()["result"]

    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "Server LLM"
