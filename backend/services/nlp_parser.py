import json
import logging
from typing import Dict, Any, Optional

from services.gemini_service import GeminiService
from models.voice_intents import (
    ParserResponse, VoiceIntent, CommandCategory,
    NavigationIntent, ControlIntent, ActionIntent,
    QueryIntent, EmergencyIntent
)

logger = logging.getLogger(__name__)

VOICE_NLP_PROMPT = """
You are the MINDFORGE NLP Parser. Your job is to convert free-form voice commands into structured JSON intents.

CATEGORIES & INTENTS:
1. navigation: go_to_url, history_back, history_forward, focus_element
2. control: start, pause, resume, stop, status, config
3. action: click, input, submit, upload
4. query: question, progress, help
5. emergency: panic, reset, override

RULES:
- Extract all relevant entities (urls, element names, text, values).
- Set priority: 0 (Panic), 1 (Signal/Stop), 2 (High), 3 (Normal), 4 (Low).
- requires_confirmation: True for 'submit', 'panic', 'reset', or any destructive action.
- suggested_response: A brief verbal confirmation (e.g., "Navigating to Google.").

OUTPUT FORMAT (JSON Only):
{{
    "category": "category_name",
    "intent": "intent_name",
    "parameters": {{}},
    "priority": 0-4,
    "requires_confirmation": boolean,
    "suggested_response": "string"
}}

COMMAND: "{command}"
"""

class NaturalLanguageParser:
    def __init__(self):
        self.gemini = GeminiService()

    async def parse(self, text: str) -> ParserResponse:
        """
        Parses raw text into a structured VoiceIntent using Gemini.
        """
        logger.info(f"Parsing voice command: {text}")
        try:
            prompt = VOICE_NLP_PROMPT.format(command=text)
            response_text = self.gemini.answer_question(prompt)
            
            # Clean up JSON formatting
            clean_json = response_text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            data = json.loads(clean_json)
            
            # Map back to models
            intent = VoiceIntent(
                category=data["category"],
                intent=data["intent"],
                parameters=data.get("parameters", {}),
                priority=data.get("priority", 3),
                original_text=text,
                requires_confirmation=data.get("requires_confirmation", False),
                suggested_response=data.get("suggested_response", "Command received.")
            )
            
            return ParserResponse(
                success=True,
                intent=intent,
                suggested_response=intent.suggested_response
            )
            
        except Exception as e:
            logger.error(f"NLP Parsing failed: {e}")
            return ParserResponse(
                success=False,
                error=str(e),
                suggested_response="I'm sorry, I couldn't understand that command."
            )
