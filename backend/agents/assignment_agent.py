"""
MINDFORGE — Assignment Agent Tools
LangChain tool definitions for reading and answering assignment questions
using Google Gemini via the GeminiService.
"""
import logging
from typing import List

from langchain_core.tools import tool

from services.gemini_service import GeminiService

logger = logging.getLogger(__name__)
_gemini = GeminiService()


@tool
def answer_question(question: str) -> str:
    """
    Generate a high-quality, accurate answer to an assignment question.
    Pass the full question text including any context or options provided.
    """
    try:
        return _gemini.answer_question(question)
    except Exception as e:
        return f"ERROR generating answer: {e}"


@tool
def answer_multiple_choice(question: str, options: str) -> str:
    """
    Select the best answer for a multiple-choice question.
    Pass the question text and the options as a string (e.g. 'A) ... B) ... C) ...').
    Returns the letter and brief justification.
    """
    try:
        prompt = f"Question: {question}\n\nOptions:\n{options}\n\nSelect the best answer and briefly justify."
        return _gemini.answer_question(prompt)
    except Exception as e:
        return f"ERROR answering MCQ: {e}"


@tool
def summarize_text(text: str, max_words: int = 150) -> str:
    """Summarize a block of text in the given maximum number of words."""
    try:
        prompt = f"Summarize the following text in at most {max_words} words:\n\n{text}"
        return _gemini.answer_question(prompt)
    except Exception as e:
        return f"ERROR summarizing: {e}"


@tool
def solve_math_problem(problem: str) -> str:
    """
    Solve a math problem. Show step-by-step working and the final answer.
    """
    try:
        prompt = f"Solve this math problem step by step:\n\n{problem}"
        return _gemini.answer_question(prompt)
    except Exception as e:
        return f"ERROR solving math: {e}"


@tool
def write_essay(topic: str, word_count: int = 300, style: str = "academic") -> str:
    """
    Write an essay on the given topic with the specified word count and style.
    Style options: academic, persuasive, descriptive, narrative.
    """
    try:
        prompt = (
            f"Write a {style} essay on the topic: '{topic}'. "
            f"Target approximately {word_count} words. "
            f"Include an introduction, body paragraphs, and conclusion."
        )
        return _gemini.answer_question(prompt)
    except Exception as e:
        return f"ERROR writing essay: {e}"


def get_assignment_tools() -> List:
    """Return all assignment tools for the orchestrator."""
    return [
        answer_question,
        answer_multiple_choice,
        summarize_text,
        solve_math_problem,
        write_essay,
    ]
