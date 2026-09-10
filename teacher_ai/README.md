# Teacher AI Assistant MVP

A working multi-agent Teacher AI Assistant built on **Google ADK 2.8.0** with real agent execution, local RAG, and session-based memory.

## Features

- **Single Agent**: Real Google ADK `Agent` executing via `Runner`
- **Multi-Agent**: Sequential pipeline with 4 specialized agents
- **RAG**: Lightweight keyword-based curriculum retrieval
- **Memory**: Session state persists teacher preferences across turns
- **Tests**: Unit tests verifying orchestration and memory

## Architecture

```
User Request
    │
    ▼
┌─────────────────────────────────────┐
│         Multi-Agent Pipeline        │
│                                     │
│  CurriculumAgent → SpecialistAgent → ReviewerAgent  │
│   (RAG lookup)      (lesson/quiz)     (validation)  │
└─────────────────────────────────────┘
    │
    ▼
Teacher Assistant Agent (single-agent mode)
    │
    ▼
Real ADK execution via google.adk.Runner
```

## Prerequisites

```bash
pip install google-adk google-genai
```

Set `GEMINI_API_KEY` environment variable for live execution:
```bash
export GEMINI_API_KEY="your-key-here"
```

## Running

### Single Agent Demo
```bash
python -m teacher_ai.app.teacher_assistant --mode single
```

### Multi-Agent Demo
```bash
python -m teacher_ai.app.teacher_assistant --mode multi --request "Create a lesson plan on photosynthesis"
```

### Tests
```bash
python -m pytest teacher_ai/tests/ -v
```

## Key Design Decisions

1. **Real ADK Execution**: Uses `google.adk.Runner.run()` with actual `Agent` objects — no simulated responses
2. **Session State**: Preferences stored in `Session.state` dict, accessible across turns
3. **Local RAG**: Keyword matching against `CURRICULUM_DOCS` (documented as lightweight retrieval)
4. **Sequential Orchestration**: Curriculum → Specialist → Reviewer pipeline with real agent-to-agent handoff
5. **Model**: Uses `gemini-3.6-flash` (updated from deprecated `gemini-3.6-flash`)

## Documentation

See `docs/` for detailed architecture, framework comparison, and interview notes.
