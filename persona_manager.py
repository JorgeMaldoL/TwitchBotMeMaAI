import json

class PersonaManager:
    SETTINGS_FILE = "ai_persona.json"

    def __init__(self):
        self.personalities = self.load_persona()

    def load_persona(self):
        try:
            with open(self.SETTINGS_FILE, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return{}
        
    def save_persona(self, channel: str, new_persona: str):
        self.personalities[channel] = f"You are a {new_persona}"
        with open(self.SETTINGS_FILE, "w")as f:
            json.dump(self.personalities, f)

    def get_persona(self, channel:str) -> str:
        return self.personalities.get(channel, "Your a nice slightly southern lady that likes to lightheartedly sarcasticly crack jokes at people.")