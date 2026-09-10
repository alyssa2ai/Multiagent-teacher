# Teacher AI Assistant Architecture

## Overview

This MVP implements a Teacher AI Assistant using **Google ADK 2.8.0** with:
- Real ADK Agent execution via `google.adk.Runner`
- Single-agent and multi-agent modes
- Local curriculum RAG (keyword-based retrieval)
- Session-based memory/state persistence
- Sequential agent orchestration

## System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Teacher AI Assistant                      │
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  Single-Agent │    │ Multi-Agent  │    │   Curriculum │  │
│  │   Mode       │    │    Mode      │    │   Knowledge  │  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘  │
│         │                   │                   │          │
│         └───────────────────┴───────────────────┘          │
│                           │                                │
│                   ┌───────▼───────┐                        │
│                   │  ADK Runner   │                        │
│                   │  (Execution)  │                        │
│                   └───────┬───────┘                        │
│                           │                                │
│              ┌────────────▼────────────┐                   │
│              │   google.adk.Agent      │                   │
│              │   (Gemini model-backed) │                   │
│              └─────────────────────────┘                   │
└─────────────────────────────────────────────────────────────┘
```

## Key Design Decisions

### 1. Real ADK Execution
- Uses `google.adk.Runner.run()` with `auto_create_session=True`
- No simulated responses - real Agent objects execute through the ADK pipeline
- Falls back to mock mode when no API key is available (for testing)

### 2. Session-Based Memory
- Preferences stored in `Session.state` dict
- Persists across multiple calls with the same Session object
- Demonstrates teacher preference (e.g., worksheet format)

### 3. Lightweight RAG
- Keyword-based retrieval from `CURRICULUM_DOCS` dictionary
- Stores retrieved context in session state for reference
- Documented as local retrieval, not vector/embedding-based

### 4. Sequential Multi-Agent Orchestration
- Pipeline: Curriculum → Specialist → Reviewer
- Each agent receives previous output as input
- Demonstrates real agent-to-agent information flow

## Execution Flow

### Single Agent Mode
```
User Request
    │
    ▼
┌─────────────────┐
│ RAG Retrieval   │
│ (Keyword match) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Memory Check    │
│ (Session state) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Build Prompt    │
│ (RAG + Memory   │
│  + Request)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ ADK Runner      │
│ (Execute Agent) │
└─────────────────┘
```

### Multi-Agent Mode
```
User Request
    │
    ▼
┌─────────────────┐
│ CurriculumAgent │
│ (RAG lookup)    │
└────────┬────────┘
         │ Output
         ▼
┌─────────────────┐
│ Lesson/Assess.  │
│ Agent           │
│ (Generate plan) │
└────────┬────────┘
         │ Output
         ▼
┌─────────────────┐
│ ReviewerAgent   │
│ (Validate)      │
└─────────────────┘
         │
         ▼
    Final Response
```

## Technology Stack

- **Framework**: Google ADK 2.8.0
- **Model**: gemini-3.6-flash (configured in Agents)
- **Session Storage**: InMemorySessionService
- **Retrieval**: Keyword matching against CURRICULUM_DOCS
- **Testing**: unittest framework

## Limitations

1. **Local RAG**: Keyword-based, not semantic/embedding search
2. **Mock Mode**: When GEMINI_API_KEY is not set, agents return formatted placeholders
3. **No Persistence**: Session state is in-memory only (lost on restart)
4. **Sequential Only**: No parallel agent execution

These are intentional MVP constraints that can be extended in future iterations.
