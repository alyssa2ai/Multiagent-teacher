# Architecture Decisions

## ADR-001: Use Google ADK Over LangChain/AutoGen

**Context**: Need to choose an agent framework for the MVP.

**Decision**: Use Google ADK 2.8.0.

**Rationale**:
- Interview assignment specifically mentioned Google ADK
- Native Gemini integration reduces complexity
- Official framework means better long-term support
- Simpler API for basic agent execution

**Consequences**:
- + Tightly coupled to Google ecosystem
- + Good for Gemini-focused applications
- - Less community resources than LangChain
- - Need to learn ADK-specific patterns (e.g., session_service requirement)

## ADR-002: Sequential Multi-Agent Pipeline

**Context**: Need to demonstrate multi-agent orchestration.

**Decision**: Use sequential pipeline: Curriculum → Specialist → Reviewer.

**Rationale**:
- Simplest form of orchestration to implement and understand
- Clear data flow between agents
- Easy to debug and explain
- Demonstrates real agent-to-agent information flow

**Consequences**:
- + Easy to follow and modify
- + Each agent has clear responsibility
- - No parallel execution (slower for independent tasks)
- - No feedback loops (reviewer can't send back to generator)
- - No dynamic routing (hardcoded logic in coordinator)

**Alternative Considered**: Workflow graph with `google.adk.Workflow`.
**Rejected Because**: More complex to implement; sequential pipeline sufficient for MVP.

## ADR-003: In-Memory Session Service

**Context**: Need session/state management for memory persistence.

**Decision**: Use `InMemorySessionService`.

**Rationale**:
- No external dependencies (no database setup)
- Sufficient for demo/testing
- Easy to understand and modify

**Consequences**:
- + Zero infrastructure setup
- + State persists across function calls in same process
- - State lost on restart
- - Not suitable for production (no durability)

**Alternative Considered**: PostgreSQL/SQLite with `DatabaseSessionService`.
**Rejected Because**: Adds infrastructure complexity for MVP.

## ADR-004: Keyword-Based Local RAG

**Context**: Need retrieval augmentation for curriculum context.

**Decision**: Use keyword matching against `CURRICULUM_DOCS` dictionary.

**Rationale**:
- No external services required (no embedding model, no vector DB)
- Deterministic and predictable
- Easy to understand and debug
- Sufficient for small knowledge base

**Consequences**:
- + No dependencies beyond ADK
- + Exact match retrieval is reliable
- - No semantic understanding (won't find "chlorophyll process" for photosynthesis)
- - Limited scalability (dictionary lookup doesn't scale well)

**Alternative Considered**: Vector embeddings with text-embedding-004 + vector store.
**Rejected Because**: Adds embedding model dependency and vector database for MVP.

## ADR-005: Mock Mode Fallback

**Context**: Need to support testing without API key.

**Decision**: Detect missing/fake API key and return formatted placeholder responses.

**Rationale**:
- Allows testing and demonstration without API costs
- Clear indication of mock mode in output
- Tests can verify structure without real LLM calls

**Consequences**:
- + Tests run without API key
- + Clear separation between real and mock execution
- - Not a substitute for real execution testing
- - Mock responses don't exercise LLM capabilities

**Implementation**:
```python
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key or api_key == "fake":
    return "(mocked response)"
```

## ADR-006: gemini-3.6-flash Model

**Context**: Need to choose a Gemini model.

**Decision**: Use `gemini-3.6-flash`.

**Rationale**:
- Current stable version
- Fast and cost-effective
- Suitable for teacher assistant use case
- Good balance of quality and speed

**Alternatives Considered**:
- `gemini-2.0-flash`: Deprecated, removed from config
- `gemini-pro`: More capable but slower/more expensive
- `gemini-2.5-pro`: Newer but may not be fully supported yet
