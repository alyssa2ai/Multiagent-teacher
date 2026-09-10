# Framework Comparison

## Google ADK vs Alternatives

### Google ADK (Our Choice)

**Pros:**
- Official Google framework for building AI applications
- Native integration with Gemini models
- Built-in session/state management
- Agent orchestration primitives
- Tool/function calling support
- Event-driven architecture
- Well-documented

**Cons:**
- Relatively new (mature but less battle-tested)
- Requires Google infrastructure dependency
- Limited community resources compared to mature frameworks
- `Runner` requires `session_service` (learned this the hard way)

**Best For:**
- Applications tightly integrated with Google Cloud/Gemini
- Rapid prototyping with Google's ecosystem
- When you need official Google support

### LangChain/LangGraph

**Pros:**
- Mature, large community
- Extensive documentation and tutorials
- Framework-agnostic (works with any LLM provider)
- Rich tool/ecosystem
- Visual debugging tools

**Cons:**
- Steeper learning curve
- More boilerplate code
- Less opinionated (more decisions to make)

**Best For:**
- Production applications needing flexibility
- Multi-provider LLM strategies
- Complex graph-based workflows

### CrewAI

**Pros:**
- Agent-centric design
- Simple role-playing paradigm
- Good for task delegation scenarios
- Active community

**Cons:**
- Less flexible for custom orchestration
- Tightly coupled to their abstraction
- Smaller ecosystem

**Best For:**
- Task-oriented agent teams
- Simpler orchestration patterns
- Quick agent deployment

### AutoGen (Microsoft)

**Pros:**
- Strong multi-agent conversation patterns
- Good for research/creative tasks
- Flexible conversation flows
- Microsoft backing

**Cons:**
- Different abstraction model
- Less opinionated about deployment
- Smaller community than LangChain

**Best For:**
- Conversational multi-agent systems
- Research/exploration tasks
- Dynamic conversation patterns

## Why ADK for This MVP?

1. **Interview Context**: Demonstrates knowledge of Google's official framework
2. **Simplicity**: Lower ceremony than LangChain for basic use cases
3. **Native Gemini**: Direct access to Gemini models without wrapper
4. **Future-Proof**: Official Google support means ongoing development
5. **Real Execution**: Uses actual ADK Runner, not just Agent definitions

## Technical Decisions

- Used `Runner.run()` instead of direct `Agent.run()` for proper session handling
- `InMemorySessionService` for simplicity (no external DB dependency)
- Sequential pipeline instead of workflow graph (simpler for MVP)
- Keyword-based RAG instead of embeddings (no external services)
