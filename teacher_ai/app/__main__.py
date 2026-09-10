"""__main__ entry point for teacher_ai module."""
import sys
from teacher_ai.app.teacher_assistant import run_single_agent, run_multi_agent
from google.adk.agents.invocation_context import Session


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Teacher AI Assistant MVP")
    parser.add_argument("--mode", choices=["single", "multi"], default="single")
    parser.add_argument("--request", default="Create a worksheet on photosynthesis")
    args = parser.parse_args()

    session = Session(id="demo_session", app_name="teacher_ai", user_id="teacher_user")

    if args.mode == "single":
        print("\n=== Single Agent Demo ===")
        # Turn 1: Set preference
        print(run_single_agent("My preferred worksheet format is 10 MCQs.", session))
        # Turn 2: Use preference
        print(run_single_agent(args.request, session))

    elif args.mode == "multi":
        print("\n=== Multi-Agent Demo ===")
        print(run_multi_agent(args.request, session))


if __name__ == "__main__":
    main()
