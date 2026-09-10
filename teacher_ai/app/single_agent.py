import os
from google import genai
from google.genai import types

class TeacherAssistant:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required.")
        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-3.6-flash"

    def chat(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        return response.text

if __name__ == "__main__":
    assistant = TeacherAssistant()
    print("Teacher Assistant Initialized (Single Agent)")
    try:
        print(assistant.chat("Create a Grade 8 science lesson plan on photosynthesis."))
    except Exception as e:
        print(f"Error: {e}")
