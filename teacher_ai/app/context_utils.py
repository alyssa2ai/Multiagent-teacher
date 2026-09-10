from google.adk import Context

def get_context() -> Context:
    return Context()

def store_memory(context: Context, key: str, value: str):
    context.store(key, value)

def retrieve_memory(context: Context, key: str) -> str:
    return context.retrieve(key)