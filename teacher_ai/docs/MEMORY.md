# Teacher AI Assistant Memory

## Session-Based State Management

Memory in this MVP is implemented through Google ADK's session state mechanism.

### How It Works

```python
from google.adk.agents.invocation_context import Session
from teacher_ai.app.teacher_assistant import run_single_agent

# Create a session
session = Session(id="my_session", app_name="teacher_ai", user_id="teacher")

# Turn 1: Set preference
result1 = run_single_agent("My preferred worksheet format is 10 MCQs", session)
# → "Memory updated: Preferred worksheet format is now set to '10 MCQs'."

# Turn 2: Use preference
result2 = run_single_agent("Create a worksheet on cells", session)
# → Agent response includes "10 MCQs" in the output
```

### State Storage

Preferences are stored in `session.state` dictionary:
```python
session.state["worksheet_format"] = "10 MCQs"
session.state["last_retrieved_standard"] = "Curriculum Standard 8.SCI.2..."
```

### Memory Lifecycle

1. **Set**: User provides preference → stored in `Session.state`
2. **Retrieve**: Agent reads from `session.state.get("key", "default")`
3. **Persist**: Same Session object maintains state across calls
4. **Reset**: New Session object starts with empty state

### Demonstration

```
Turn 1: "My preferred worksheet format is 10 MCQs."
        → Sets session.state["worksheet_format"] = "10 MCQs"

Turn 2: "Create a worksheet on photosynthesis."
        → Reads session.state["worksheet_format"]
        → Passes to agent as part of prompt context
        → Agent generates response using the preference
```

## RAG Context as Transient Memory

The curriculum retrieval also acts as transient memory:
```python
# In _retrieve_curriculum()
session.state["last_retrieved_standard"] = doc
```

This allows the agent to reference the retrieved standard in its response.

## Limitations

- **In-Memory Only**: State is lost when the program exits
- **No History**: Only the latest preference is stored (not a history)
- **Single User**: Session is tied to one user_id

For production, replace with a database-backed session service.
