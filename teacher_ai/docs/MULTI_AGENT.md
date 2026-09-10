# Multi-Agent Architecture

## Design

Sequential pipeline orchestration with specialist agents:

```
Teacher Request
    │
    ▼
┌─────────────────────────────────────────────┐
│           ADKCoordinator                    │
│                                             │
│  1. CurriculumAgent    → Retrieves standard │
│  2. Lesson/AssessAgent → Generates content  │
│  3. ReviewerAgent      → Validates output   │
└─────────────────────────────────────────────┘
    │
    ▼
Final Response
```

## Agent Responsibilities

### CurriculumAgent
- **Input**: Topic/request
- **Output**: Curriculum standard/context
- **Instruction**: "Retrieve and summarize Grade 8 science curriculum standards"

### LessonPlannerAgent OR AssessmentAgent
- **Selection**: Based on request type ("lesson" → LessonPlanner, "quiz"/"mcq" → Assessment)
- **Output**: Structured content (lesson plan or quiz)
- **Instruction**: Varies by specialization

### ReviewerAgent
- **Input**: Previous agent's output
- **Output**: Validation feedback
- **Instruction**: "Review for pedagogical accuracy and adherence to preferences"

## Information Flow

Real agent-to-agent communication:
```python
# Step 1: Curriculum
curr_output = curriculum_agent.run(curriculum_prompt, context=context)

# Step 2: Specialized (uses Step 1 output)
agent_output = specialist_agent.run(request, context=context)

# Step 3: Review (uses Step 2 output)
final_review = reviewer_agent.run(f"Review: {agent_output}", context=context)
```

## Orchestration Pattern

The coordinator (`ADKCoordinator`) manages:
1. **Routing**: Determines which specialist agent to use
2. **Chaining**: Passes output from one agent to the next
3. **Aggregation**: Combines all outputs into final response

## Why Sequential?

1. **Simplicity**: Easier to debug and understand
2. **Predictability**: Output of each step is deterministic
3. **MVP Scope**: Demonstrates orchestration without complexity
4. **Real Execution**: Each agent actually runs through ADK pipeline

## Limitations

- No parallel execution
- No feedback loops
- No dynamic routing decisions by agents themselves
- No workflow graph (uses code-based sequencing)

These can be addressed with `google.adk.Workflow` in future iterations.
