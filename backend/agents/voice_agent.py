"""
MINDFORGE — Voice Agent
Processes voice commands: speech-to-text + intent parsing into structured tasks.
"""
import logging
from typing import Dict, Any, Optional

from services.voice_service import VoiceService
from services.gemini_service import GeminiService

logger = logging.getLogger(__name__)

INTENT_PROMPT = """You are a command parser for MINDFORGE, an AI assignment automation system.
Parse the following voice command into a structured JSON task.

Voice command: "{command}"

Return ONLY valid JSON with this structure:
{{
    "action": "navigate|fill|submit|answer|summarize|write|screenshot|status",
    "target": "URL or element description or topic",
    "parameters": {{
        "additional": "key-value parameters as needed"
    }},
    "priority": "high|normal|low",
    "natural_language": "reformulated natural language description of the task"
}}"""


class VoiceAgent:
    def __init__(self):
        self.voice_service = VoiceService()
        self.gemini = GeminiService()

    def listen(self, timeout: int = 10) -> Optional[str]:
        """Listen for a voice command and return the transcribed text."""
        logger.info("🎤 Listening for voice command...")
        transcript = self.voice_service.listen(timeout=timeout)
        if transcript:
            logger.info(f"Transcript: {transcript}")
        return transcript

    def parse_intent(self, command: str) -> Dict[str, Any]:
        """
        Parse a natural language voice command into a structured intent.
        Returns a dict with action, target, parameters, priority.
        """
        import json
        try:
            prompt = INTENT_PROMPT.format(command=command)
            raw = self.gemini.answer_question(prompt)
            # Strip markdown code fences if present
            raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            return json.loads(raw)
        except Exception as e:
            logger.warning(f"Intent parsing failed, returning raw command: {e}")
            return {
                "action": "unknown",
                "target": command,
                "parameters": {},
                "priority": "normal",
                "natural_language": command,
            }

    def speak(self, text: str) -> None:
        """Convert text to speech and play it."""
        self.voice_service.speak(text)

    async def process_command(self, command: str) -> Dict[str, Any]:
        """Full pipeline: parse intent → return structured task."""
        intent = self.parse_intent(command)
        logger.info(f"🎯 Parsed intent: {intent}")
        return intent
