"""Tests for teacher AI assistant."""
import unittest
from google.adk.agents.invocation_context import Session
from teacher_ai.app.teacher_assistant import run_single_agent, run_multi_agent


class TestTeacherAI(unittest.TestCase):
    """Test cases for single and multi-agent execution."""

    def test_single_agent_memory(self):
        """Test that worksheet format preference persists in session state."""
        session = Session(id="test_001", app_name="teacher_ai", user_id="teacher")
        result = run_single_agent("My preferred worksheet format is 10 MCQs", session)
        self.assertIn("Memory updated", result)
        self.assertEqual(session.state.get("worksheet_format"), "10 MCQs")

    def test_single_agent_rag(self):
        """Test that RAG context is included in agent prompt."""
        session = Session(id="test_002", app_name="teacher_ai", user_id="teacher")
        result = run_single_agent("Create a worksheet on photosynthesis", session)
        self.assertIn("photosynthesis", result.lower())
        self.assertIn("Curriculum", result)

    def test_single_agent_preference_used(self):
        """Test that stored preference is passed to agent."""
        session = Session(id="test_003", app_name="teacher_ai", user_id="teacher")
        run_single_agent("My preferred worksheet format is 10 MCQs", session)
        result = run_single_agent("Create a worksheet on cells", session)
        self.assertIn("10 MCQs", result)

    def test_multi_agent_lesson_flow(self):
        """Test multi-agent pipeline for lesson plan request."""
        session = Session(id="test_004", app_name="teacher_ai", user_id="teacher")
        result = run_multi_agent("Create a lesson plan on photosynthesis", session)
        self.assertIn("CurriculumAgent", result)
        self.assertIn("LessonPlannerAgent", result)
        self.assertIn("ReviewerAgent", result)

    def test_multi_agent_quiz_flow(self):
        """Test multi-agent pipeline for quiz request."""
        session = Session(id="test_005", app_name="teacher_ai", user_id="teacher")
        result = run_multi_agent("Create 10 MCQs on cells", session)
        self.assertIn("AssessmentAgent", result)
        self.assertIn("ReviewerAgent", result)


if __name__ == "__main__":
    unittest.main()
