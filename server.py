import asyncio
import websockets
import re
from constants import *
from ai_manager import AIManager
from persona_manager import PersonaManager

class TwitchBot:
    def __init__(self, oauth_token: str, bot_username: str, channel_url: str, ws_url: str, openai_api_key: str):
        self.oauth_token = oauth_token
        self.bot_username = bot_username
        self.channel_url = channel_url
        self.ws_url = ws_url
        self.ai_manager = AIManager(openai_api_key)
        self.personality_manager = PersonaManager()

    async def connect(self):
        try:
            async with websockets.connect(self.ws_url) as ws:
                print("Connected to Twitch's websocket")

                # Request capabilities (optional, but often helpful)
                await ws.send("CAP REQ :twitch.tv/membership\r\n")
                await ws.send("CAP REQ :twitch.tv/tags\r\n")
                await ws.send("CAP REQ :twitch.tv/commands\r\n")

                # Send authentication info
                await ws.send(f"PASS {self.oauth_token}\r\n")
                await ws.send(f"NICK {self.bot_username}\r\n")
                await ws.send(f"JOIN {self.channel_url}\r\n")
                print(f"-> Joined {self.channel_url}")

                await self._handle_messages(ws)
        except Exception as e:
            print(f"Exception in connect_to_twitch: {e}")
            raise

    async def _handle_messages(self, ws):
        while True:
            response = await ws.recv()
            print(f"Received message: {response}")

            if "PING" in response:
                await ws.send("PONG :tmi.twitch.tv\r\n")
                print("-> sent PONG to Twitch")
                continue

            match = re.search(r":(\w+)!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :(.*)", response)
            if match:
                username, message = match.groups()
                print(f"{username}: {message}")
                
                await self.commands(username, message, ws)

    async def commands(self, username, message, ws):
        message = message.strip().lower()

        if message == "!hello":
            reply = f"PRIVMSG {self.channel_url} :*Your MeMa Looks at {username} with loving eyes*, Hello Sweetie!\r\n"
            await ws.send(reply)
            print(f"Bot: {reply}")
            await asyncio.sleep(1)

        elif message.startswith("!persona"):
            new_persona = message.replace("!persona", "").strip()
            self.personality_manager.save_persona(self.channel_url, new_persona)
            reply = f"PRIVMSG {self.channel_url} :AI persona changed to '{new_persona}'\r\n"
            await ws.send(reply)
            print(f"Personality set to: {new_persona}.")
            await asyncio.sleep(1)

        elif message.startswith("!mema"):
            users_prompt = message.replace("!mema", "").strip()
            openai_replies = self.ai_manager.get_ai_response(users_prompt, self.channel_url)
            reply = f"PRIVMSG {self.channel_url} :{openai_replies}\r\n"
            await ws.send(reply)
            print(f"Bot: {reply}")
            await asyncio.sleep(0)

