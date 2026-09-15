import os
import asyncio
import random
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from google import genai

API_ID = int(os.environ.get("API_ID", 6))
API_HASH = os.environ.get("API_HASH", "eb0663579128e5f5337021e028b0304c")
GEMINI_KEY = os.environ.get("GEMINI_KEY")
TARGET_CHAT_ID = int(os.environ.get("TARGET_CHAT_ID"))
SESSION_STRING = os.environ.get("SESSION_STRING")

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
ai_client = genai.Client(api_key=GEMINI_KEY)

@client.on(events.NewMessage(chats=TARGET_CHAT_ID))
async def handle_new_message(event):
    if event.out or not event.text:
        return

    await asyncio.sleep(random.uniform(3, 8))

    try:
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=event.text,
            config={'system_instruction': "Отвечай кратко и дружелюбно."}
        )
        if response.text:
            await event.reply(response.text)
    except Exception as e:
        print(f"Ошибка: {e}")

print("Бот запущен...")
client.start()
client.run_until_disconnected()
