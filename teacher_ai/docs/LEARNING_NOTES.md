# Learning Notes

A beginner-friendly technical guide to concepts in the Teacher AI Assistant MVP.

## Key Concepts

* **Google ADK (`google.adk`):** Google's official Agent Development Kit providing primitives like `Agent`, `Context`, `Event`, and `Runner` for building agentic AI applications.
* **Agent:** An autonomous system built around an LLM that maintains state, executes instructions, and collaborates with other agents.
* **Multi-Agent System:** A system of multiple specialized agents where each agent handles a specific domain task (e.g., curriculum vs. assessment).
* **Sequential Orchestration:** Passing outputs step-by-step from one agent to another (e.g., Retrieval → Planning → Review).
* **RAG (Retrieval-Augmented Generation):** Injecting retrieved domain documents into prompt context to ground the LLM's answer in factual sources.
* **Session Memory:** Storing session-scoped user preferences to customize future outputs dynamically.

## What Our Application Provides
* Real `google-adk` package imports.
* Specialized agent definitions using `google.adk.Agent`.
* Sequential multi-agent information passing.
* Session-state tracking for user preferences.
