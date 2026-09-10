# Teacher AI Assistant RAG (Retrieval Augmented Generation)

## Implementation

This MVP uses **lightweight keyword-based local retrieval** as the RAG mechanism.

### Knowledge Base

```python
CURRICULUM_DOCS = {
    "photosynthesis": "Curriculum Standard 8.SCI.4: ...",
    "cells": "Curriculum Standard 8.SCI.2: ...",
    "ecosystems": "Curriculum Standard 8.SCI.6: ..."
}
```

### Retrieval Logic

```python
def _retrieve_curriculum(query: str, session: Session) -> str:
    query_lower = query.lower()
    for key, doc in CURRICULUM_DOCS.items():
        if key in query_lower:
            session.state["last_retrieved_standard"] = doc
            return doc
    return "No specific curriculum standard matched..."
```

### Usage in Agent Prompt

```python
curriculum_context = _retrieve_curriculum(prompt, session)
full_prompt = (
    f"[Retrieved Curriculum RAG Context]: {curriculum_context}\n"
    f"[Session Memory Preference]: Worksheet format is {worksheet_format}\n"
    f"[User Request]: {prompt}"
)
```

## Why Keyword-Based?

1. **Simplicity**: No external dependencies or embeddings model required
2. **Deterministic**: Exact keyword matches, no similarity thresholds
3. **Transparency**: Easy to understand and debug
4. **Sufficient for MVP**: Small knowledge base fits local storage

## What It's Not

- ❌ NOT vector/embedding-based search
- ❌ NOT semantic similarity retrieval
- ❌ NOT using a vector database
- ❌ NOT using ADK's built-in memory service (though it's available)

## Future Enhancements

For production, consider:
1. Embedding-based retrieval (text-embedding-004)
2. Vector store (Redis, Pinecone, etc.)
3. ADK's `add_memory()` / `search_memory()` methods
4. Hybrid keyword + semantic search

## Documentation Note

This is documented as "lightweight keyword-based local retrieval" to accurately reflect what the MVP implements.
