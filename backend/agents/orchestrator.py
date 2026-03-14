"""
MINDFORGE — Orchestrator Agent
Top-level LangChain AgentExecutor that receives parsed voice commands and 
routes them to the appropriate sub-agent tools.
"""
import logging
from typing import Any, Dict

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from services.gemini_service import get_llm
from agents.browser_agent import get_browser_tools
from agents.assignment_agent import get_assignment_tools

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are MINDFORGE, an elite AI assistant specialized in automating 
online academic assignments. You have access to a suite of tools:

- Browser tools: navigate websites, fill forms, click elements, submit work
- Assignment tools: read questions, generate accurate answers using Gemini AI
- Utility tools: take screenshots, wait for page loads, extract page text

Always think step-by-step. Before acting on an assignment:
1. Confirm the target URL and assignment type
2. Navigate to the assignment
3. Read all questions carefully
4. Generate high-quality answers
5. Fill in the answers methodically
6. Review before submitting

You respond concisely and act precisely."""


def build_orchestrator() -> AgentExecutor:
    """Build and return the main orchestrator agent executor."""
    llm = get_llm()
    tools = get_browser_tools() + get_assignment_tools()

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=15,
        return_intermediate_steps=True,
        handle_parsing_errors=True,
    )


async def run_task(command: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """
    Run a voice command through the orchestrator.
    
    Args:
        command: Natural language task description from voice input
        context: Optional additional context (e.g. current URL, previous steps)
    
    Returns:
        Dict with 'output', 'steps', and 'success' keys
    """
    logger.info(f"Orchestrator received command: {command}")
    orchestrator = build_orchestrator()

    try:
        result = await orchestrator.ainvoke({
            "input": command,
            "chat_history": context.get("chat_history", []) if context else [],
        })
        return {
            "success": True,
            "output": result.get("output", ""),
            "steps": result.get("intermediate_steps", []),
        }
    except Exception as e:
        logger.error(f"Orchestrator error: {e}")
        return {"success": False, "output": str(e), "steps": []}
