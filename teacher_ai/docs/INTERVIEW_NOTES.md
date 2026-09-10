# Interview Notes - Teacher AI Assistant MVP

## Project Summary

Built a working Teacher AI Assistant MVP using Google ADK 2.8.0 demonstrating:
- Single-agent execution with RAG and memory
- Multi-agent sequential orchestration
- Real agent-to-agent information flow
- Session-based state persistence

## Key Technical Points

### What I Built
1. **Single Agent Mode**: TeacherAssistant agent with curriculum RAG and preference memory
2. **Multi-Agent Mode**: Sequential pipeline of 4 specialist agents (Curriculum → Specialist → Reviewer)
3. **Real ADK Execution**: Uses `google.adk.Runner` with actual Agent objects, not simulated responses
4. **Session State**: Preferences persist across turns using ADK's Session mechanism

### Challenges Faced and Solutions

**Challenge 1**: Understanding ADK 2.8 API
- Runner requires `session_service` parameter
- Session must be created in service before use
- Solution: Used `InMemorySessionService` with `auto_create_session=True`

**Challenge 2**: Agent execution pattern
- `Agent.run()` returns async generator, not direct result
- Solution: Use `Runner.run()` which handles async internally

**Challenge 3**: Multi-agent orchestration
- Needed to pass output from one agent to next
- Solution: Sequential pipeline with explicit result extraction

### Architecture Decisions

1. **Sequential over Parallel**: Simpler to implement and debug for MVP
2. **Local RAG**: No external dependencies, deterministic retrieval
3. **In-Memory Session**: No database setup required for demo
4. **Mock Mode**: Allows testing without API key

## Interview Questions and Answers

### Q: How does ADK differ from LangChain?
**A**: ADK is Google's official framework with native Gemini integration. LangChain is framework-agnostic with broader ecosystem. ADK has simpler API for Google-centric apps.

### Q: Why keyword-based RAG instead of embeddings?
**A**: MVP scope - eliminates external dependencies. Production would use text-embedding-004 + vector store for semantic search.

### Q: How does session state work?
**A**: Via `Session.state` dict, persisted through `InMemorySessionService`. Same session object = shared state across calls.

### Q: What's the agent execution flow?
**A**: `Runner.run()` → yields `Event` objects → extract text from `event.content.parts`

### Q: How do agents communicate?
**A**: In this MVP, sequential pipeline - output of one agent becomes input of next. More complex systems use shared session/context.

### Q: What are the limitations?
**A**: 
- No parallel execution
- No workflow graph
- Local RAG only (no semantic search)
- In-memory state (no persistence)

### Q: How would you scale this?
**A**: 
- Add vector DB for RAG
- Use Workflow for complex orchestration
- Add PostgreSQL for session persistence
- Implement feedback loops between agents

## Code Highlights

```python
# Real agent execution
runner = Runner(
    app_name="teacher_ai",
    agent=teacher_agent,
    session_service=_session_service,
    auto_create_session=True,
)
events = runner.run(user_id="teacher", session_id="session_001", new_message=...)
```

```python
# Session memory
session.state["worksheet_format"] = "10 MCQs"  # Store
session.state.get("worksheet_format")  # Retrieve
```

## Technical Depth Demonstrated

1. ✓ Google ADK 2.8.0 APIs
2. ✓ Agent definition and execution
3. ✓ Session/state management
4. ✓ Multi-agent orchestration
5. ✓ RAG implementation
6. ✓ Testing and validation
7. ✓ Documentation
