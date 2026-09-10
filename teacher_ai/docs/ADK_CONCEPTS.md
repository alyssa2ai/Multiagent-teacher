# Google ADK 2.8.0 Core Concepts

This MVP directly utilizes the official `google-adk` Python library v2.8.0.

## Installed Package

- **Package Name:** `google-adk` (v2.8.0)
- **Core Abstractions:**
  - `google.adk.Agent`: Defines an agent with name, model, and instruction
  - `google.adk.Context`: Execution context container (mostly internal)
  - `google.adk.Runner`: Orchestrates agent execution loops
  - `google.adk.Event`: Represents events in conversation flow
  - `google.adk.Workflow`: For workflow-based orchestration (not used in this MVP)

## Agent Definitions in Our Codebase

```python
from google.adk import Agent

# Single agent
teacher_agent = Agent(
    name="TeacherAssistant",
    model="gemini-3.6-flash",
    instruction="You are an expert school teacher assistant..."
)

# Multi-agent team
curriculum_agent = Agent(name="CurriculumAgent", ...)
lesson_planner_agent = Agent(name="LessonPlannerAgent", ...)
assessment_agent = Agent(name="AssessmentAgent", ...)
reviewer_agent = Agent(name="ReviewerAgent", ...)
```

## Execution Mechanism

Agents are executed through `Runner`:

```python
from google.adk import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService

runner = Runner(
    app_name="teacher_ai",
    agent=teacher_agent,
    session_service=InMemorySessionService(),
    auto_create_session=True,  # Automatically create session if needed
)

events = runner.run(
    user_id="teacher",
    session_id="session_001",
    new_message=Content(parts=[Part(text="User request")]),
)
```

## Session Management

Sessions provide persistent state and history:

```python
from google.adk.agents.invocation_context import Session

# Create session
session = Session(id="session_001", app_name="teacher_ai", user_id="teacher")

# Store preference
session.state["worksheet_format"] = "10 MCQs"

# Retrieve preference
format = session.state.get("worksheet_format", "standard")
```

## Event Processing

Runner yields `Event` objects. Extract text from events:

```python
for event in events:
    if event.content and event.content.parts:
        for part in event.content.parts:
            if part.text:
                print(part.text)
```

## Key Learnings

1. **Runner requires `session_service`**: Must provide an instance (e.g., `InMemorySessionService`)
2. **`auto_create_session=True`**: Simplifies session management
3. **Agent.run() is async**: Returns AsyncGenerator[Event, None]
4. **Runner.run() is sync wrapper**: Handles async internally, returns Generator[Event, None, None]
5. **Session state is shared**: Can be accessed by agent instructions
