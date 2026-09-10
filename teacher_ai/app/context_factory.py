from google.adk import Context, Session
from google.adk.invocation_context import InvocationContext

def create_context(user_id: str = "teacher_user", run_id: str = None, session: Session = None) -> Context:
    """Create a properly initialized ADK Context.

    Args:
        user_id: User identifier for the session
        run_id: Optional run identifier
        session: Optional Session object

    Returns:
        A fully initialized Context ready for agent execution.
    """
    if session is None:
        session = Session()
    invocation_context = InvocationContext(
        session=session,
        user_id=user_id,
        run_id=run_id or f"run_{hash(str(user_id)) % 10000}"
    )
    return Context(invocation_context=invocation_context)


def get_default_context() -> Context:
    """Get a default context for testing and demos.
    """
    return create_context()