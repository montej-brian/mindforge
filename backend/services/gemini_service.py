"""
MINDFORGE — Gemini Service
Async wrapper around the Google Gemini API via langchain-google-genai.
"""
import logging
from functools import lru_cache
from typing import Optional

from langchain_google_genai import ChatGoogleGenerativeAI
from config import settings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_llm() -> ChatGoogleGenerativeAI:
    """Return a cached Gemini LLM instance for use by all agents."""
    return ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        google_api_key=settings.gemini_api_key,
        temperature=0.3,
        max_retries=3,
        convert_system_message_to_human=True,
    )


class GeminiService:
    """High-level interface for Gemini text generation."""

    def __init__(self):
        self.llm = get_llm()

    def answer_question(self, prompt: str, system_context: Optional[str] = None) -> str:
        """
        Send a prompt to Gemini and return the text response.

        Args:
            prompt: The user prompt / question
            system_context: Optional additional system instructions

        Returns:
            Generated text response
        """
        from langchain_core.messages import HumanMessage, SystemMessage

        messages = []
        if system_context:
            messages.append(SystemMessage(content=system_context))
        messages.append(HumanMessage(content=prompt))

        logger.debug(f"Gemini request: {prompt[:100]}...")
        response = self.llm.invoke(messages)
        return response.content

    async def answer_question_async(self, prompt: str) -> str:
        """Async version of answer_question."""
        from langchain_core.messages import HumanMessage
        response = await self.llm.ainvoke([HumanMessage(content=prompt)])
        return response.content
