import asyncio  # Import the asyncio library for asynchronous programming
from constants import *
from server import TwitchBot

async def main():
    bot = TwitchBot(
        oauth_token=OAUTH_TOKEN,
        bot_username=BOT_USERNAME,
        channel_url=CHANNEL,
        ws_url=TWITCH_WS_URL,
        openai_api_key=OPENAI_API_KEY
    )

    while True:
        try:
            await bot.connect()
        except Exception as error:
            print(f"Error: {error}. Reconnecting now...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())