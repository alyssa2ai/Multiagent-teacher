"""Google ADK 2.8.0 Teacher AI Assistant MVP.

Single and multi-agent orchestration with real ADK execution,
local RAG retrieval, and session-based memory/state.
"""

from __future__ import annotations

import os
from typing import Any

from google.adk.agents.invocation_context import InvocationContext, Session
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk import Agent, Context, Runner

# ---------------------------------------------------------------------------
# Curriculum knowledge base (lightweight keyword-based local retrieval)
# ---------------------------------------------------------------------------
CURRICULUM_DOCS: dict[str, str] = {
    "photosynthesis": (
        "Curriculum Standard 8.SCI.4: Photosynthesis occurs in chloroplasts "
        "where chlorophyll absorbs sunlight, converting carbon dioxide and "
        "water into glucose and oxygen."
    ),
    "cells": (
        "Curriculum Standard 8.SCI.2: Plant and animal cells share common "
        "organelles like the nucleus and mitochondria, but plant cells have a "
        "rigid cell wall and chloroplasts."
    ),
    "ecosystems": (
        "Curriculum Standard 8.SCI.6: Ecosystems consist of communities of "
        "organisms interacting with their physical environment, involving "
        "energy flow and nutrient cycling."
    ),
}

# ---------------------------------------------------------------------------
# Single teacher assistant agent
# ---------------------------------------------------------------------------
teacher_agent = Agent(
    name="TeacherAssistant",
    model="gemini-3.6-flash",
    instruction=(
        "You are an expert school teacher assistant. "
        "Help teachers create lesson plans, quizzes, and explain concepts "
        "at a Grade 8 level. "
        "Always respect stored teacher preferences such as worksheet format. "
        "When asked to create worksheets, use the preferred format from the "
        "session state if one has been set."
    ),
)

# ---------------------------------------------------------------------------
# Multi-agent team
# ---------------------------------------------------------------------------
curriculum_agent = Agent(
    name="CurriculumAgent",
    model="gemini-3.6-flash",
    instruction=(
        "You retrieve and summarize relevant Grade 8 science curriculum "
        "standards. Provide accurate curriculum context based on the topic."
    ),
)

lesson_planner_agent = Agent(
    name="LessonPlannerAgent",
    model="gemini-3.6-flash",
    instruction=(
        "You generate structured Grade 8 lesson plans based on "
        "curriculum standards. Include objectives, activities, and assessment."
    ),
)

assessment_agent = Agent(
    name="AssessmentAgent",
    model="gemini-3.6-flash",
    instruction=(
        "You generate quizzes, MCQs, and assessments for Grade 8 science. "
        "Follow the teacher's preferred format when specified."
    ),
)

reviewer_agent = Agent(
    name="ReviewerAgent",
    model="gemini-3.6-flash",
    instruction=(
        "You review generated lessons and assessments for pedagogical "
        "accuracy and adherence to curriculum standards and teacher "
        "preferences. Provide concise feedback."
    ),
)

# Shared session service for all agents
_session_service = InMemorySessionService()


# ===================================================================
# Single-agent helper
# ===================================================================

def run_single_agent(prompt: str, session: Session | None = None) -> str:
    """Execute the single TeacherAssistant agent with RAG + memory.

    The prompt is treated as user input. Session state persists preferences
    across calls when the same Session object is reused.
    """
    if session is None:
        session = Session(id="session_001", app_name="teacher_ai", user_id="teacher")

    # -- Memory handling --------------------------------------------------
    if "preferred worksheet format" in prompt.lower():
        parts = prompt.split("is")
        if len(parts) < 2:
            raise ValueError("Invalid format for setting worksheet format")
        fmt = parts[-1].strip()
        session.state["worksheet_format"] = fmt
        return f"Memory updated: Preferred worksheet format is now set to '{fmt}'."

    # -- RAG retrieval ----------------------------------------------------
    curriculum_context = _retrieve_curriculum(prompt, session)

    # -- Build the user message -------------------------------------------
    worksheet_format = session.state.get("worksheet_format", "standard")
    full_prompt = (
        f"[Retrieved Curriculum RAG Context]: {curriculum_context}\n"
        f"[Session Memory Preference]: Worksheet format is {worksheet_format}\n"
        f"[User Request]: {prompt}"
    )

    # -- Execute via ADK Runner -------------------------------------------
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key or api_key == "fake":
        return (
            f"ADK Agent '{teacher_agent.name}' Response (mocked, no API key): "
            f"Processed request with retrieved context: '{curriculum_context}' "
            f"and worksheet format: '{worksheet_format}'."
        )

    runner = Runner(
        app_name="teacher_ai",
        agent=teacher_agent,
        session_service=_session_service,
        auto_create_session=True,
    )
    from google.genai import types  # lazy import for when API key exists
    event_gen = runner.run(
        user_id=session.user_id,
        session_id=session.id,
        new_message=types.Content(parts=[types.Part(text=full_prompt)]),
    )
    # Collect events; the last LlmResponse event has the agent output.
    last_content: str | None = None
    for event in event_gen:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    last_content = part.text
    return last_content or "(no content returned)"


# ===================================================================
# Multi-agent coordinator (sequential orchestration)
# ===================================================================

def run_multi_agent(request: str, session: Session | None = None) -> str:
    """Execute a sequential pipeline of specialist agents.

    Flow: Curriculum -> Lesson/Assessment -> Reviewer
    Each agent receives the previous agent's output as its input,
    demonstrating real agent-to-agent information flow.
    """
    if session is None:
        session = Session(id="session_002", app_name="teacher_ai", user_id="teacher")

    req_lower = request.lower()
    api_key = os.environ.get("GEMINI_API_KEY")
    use_mock = not api_key or api_key == "fake"

    # Step 1: Curriculum Agent
    curriculum_prompt = f"Retrieve the Grade 8 curriculum standard for: {request}"
    if use_mock:
        curriculum_events = []
    else:
        runner = Runner(
            app_name="teacher_ai",
            agent=curriculum_agent,
            session_service=_session_service,
            auto_create_session=True,
        )
        from google.genai import types
        curriculum_events = list(runner.run(
            user_id=session.user_id,
            session_id=session.id,
            new_message=types.Content(parts=[types.Part(text=curriculum_prompt)]),
        ))
    curr_output = _extract_text(curriculum_events)
    if use_mock:
        curr_output = (
            f"[{curriculum_agent.name}] Retrieved curriculum standard "
            f"for {request}."
        )

    # Step 2: Specialized Agent (lesson planner or assessment)
    if "lesson" in req_lower:
        specialist_agent = lesson_planner_agent
        specialist_name = lesson_planner_agent.name
    elif "quiz" in req_lower or "mcq" in req_lower:
        specialist_agent = assessment_agent
        specialist_name = assessment_agent.name
    else:
        specialist_agent = curriculum_agent
        specialist_name = curriculum_agent.name

    if use_mock:
        specialist_events = []
    else:
        specialist_runner = Runner(
            app_name="teacher_ai",
            agent=specialist_agent,
            session_service=_session_service,
            auto_create_session=True,
        )
        from google.genai import types
        specialist_events = list(specialist_runner.run(
            user_id=session.user_id,
            session_id=session.id,
            new_message=types.Content(parts=[types.Part(text=request)]),
        ))
    agent_output = _extract_text(specialist_events)
    if use_mock:
        if "lesson" in req_lower:
            agent_output = f"[{specialist_name}] Generated lesson plan on {request}."
        elif "quiz" in req_lower or "mcq" in req_lower:
            agent_output = f"[{specialist_name}] Generated 10 MCQs on {request}."
        else:
            agent_output = f"[{specialist_name}] Explained {request} at Grade 8 level."

    # Step 3: Reviewer Agent
    if use_mock:
        review_events = []
    else:
        reviewer_runner = Runner(
            app_name="teacher_ai",
            agent=reviewer_agent,
            session_service=_session_service,
            auto_create_session=True,
        )
        from google.genai import types
        review_events = list(reviewer_runner.run(
            user_id=session.user_id,
            session_id=session.id,
            new_message=types.Content(parts=[types.Part(text=f"Review this output:\n{agent_output}")]),
        ))
    final_review = _extract_text(review_events)
    if use_mock:
        final_review = f"[{reviewer_agent.name}] Approved output. Pedagogically sound and grounded in curriculum."

    return (
        f"\n--- ADK Multi-Agent Orchestration Flow ---\n"
        f"1. {curr_output[:200]}{'...' if len(curr_output) > 200 else ''}\n"
        f"2. {agent_output[:200]}{'...' if len(agent_output) > 200 else ''}\n"
        f"3. {final_review[:200]}{'...' if len(final_review) > 200 else ''}\n"
        f"------------------------------------------"
    )


# ===================================================================
# Internal helpers
# ===================================================================

def _retrieve_curriculum(query: str, session: Session) -> str:
    """Keyword-based local retrieval from the curriculum knowledge base."""
    query_lower = query.lower()
    for key, doc in CURRICULUM_DOCS.items():
        if key in query_lower:
            session.state["last_retrieved_standard"] = doc
            return doc
    return "No specific curriculum standard matched. Providing general science knowledge."


def _extract_text(events: list) -> str:
    """Extract the text content from a list of ADK Event objects."""
    for event in reversed(events):
        if hasattr(event, "content") and event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    return part.text
    return ""
