import os
from google.adk import Agent, Context
from teacher_ai.app.context_factory import get_default_context

# Specialized ADK Agents for Multi-Agent Orchestration
curriculum_agent = Agent(
    name="CurriculumAgent",
    model="gemini-3.6-flash",
    instruction="You retrieve and summarize curriculum standards for Grade 8 science."
)

lesson_planner_agent = Agent(
    name="LessonPlannerAgent",
    model="gemini-3.6-flash",
    instruction="You generate structured Grade 8 lesson plans based on curriculum standards."
)

assessment_agent = Agent(
    name="AssessmentAgent",
    model="gemini-3.6-flash",
    instruction="You generate quizzes, MCQs, and assessments for Grade 8 science."
)

reviewer_agent = Agent(
    name="ReviewerAgent",
    model="gemini-3.6-flash",
    instruction="You review generated lessons and assessments for pedagogical accuracy and adherence to preferences."
)


class ADKCoordinator:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")

    def coordinate(self, request: str, context: Context = None) -> str:
        if context is None:
            context = get_default_context()

        req_lower = request.lower()

        # Step 1: Curriculum / RAG invocation
        curriculum_prompt = f"Retrieve the Grade 8 curriculum standard for: {request}"
        curr_output = curriculum_agent.run(curriculum_prompt, context=context)

        # Step 2: Specialized Agent Delegation
        if "lesson" in req_lower:
            agent_output = lesson_planner_agent.run(request, context=context)
        elif "quiz" in req_lower or "mcq" in req_lower:
            agent_output = assessment_agent.run(request, context=context)
        else:
            agent_output = curriculum_agent.run(request, context=context)

        # Step 3: Reviewer Agent validation (Agent-to-Agent Information Flow)
        final_review = reviewer_agent.run(f"Review this output: {agent_output.content}", context=context)

        return f"\n--- ADK Multi-Agent Orchestration Flow ---\n1. Curriculum: {curr_output.content[:200]}...\n2. Generated: {agent_output.content[:200]}...\n3. Review: {final_review.content[:200]}...\n------------------------------------------"


if __name__ == "__main__":
    print("--- Testing ADK Multi-Agent Orchestration ---")
    context = get_default_context()
    coord = ADKCoordinator()
    print(coord.coordinate("Create a lesson plan on photosynthesis.", context))
    print(coord.coordinate("Create 10 MCQs on photosynthesis.", context))