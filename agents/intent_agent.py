# intent_agent.py
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client()

class IntentAgent:
    def detect_intent(self, query):
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction="You are a FAQ intent classification agent. Classify user intent from this query in one word or short phrase",),
            contents=query
        )
        print("Intent Detection Response:", response.text.strip().lower())
        return response.text.strip().lower()
