import openai
from persona_manager import PersonaManager
from constants import *

class AIManager:
    def __init__(self, api_key: str):
        self.persona_manager = PersonaManager()
        openai.api_key = api_key

    def get_ai_response(self, twitch_message: str, channel: str) -> str:
        personality = self.persona_manager.get_persona(channel)
        response = openai.chat.completions.create(
            model="gpt-4.5-preview",  # Specifies the GPT-4 model for the chat completion
            messages=[
                {"role": "system", "content": f"{PERSONA_PROMPT}, {personality}"},  # System prompt defining the AI's role
                {"role": "user", "content": twitch_message},  # The use 's input from Twitch chat
            ],
            temperature=0.7,
            max_tokens=100)
        # OpenAI returns a complex response structure. We extract the content from the first choice in the response.
        return response.choices[0].message.content