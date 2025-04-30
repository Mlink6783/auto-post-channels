import asyncio
from fastapi import FastAPI
from telegram import Bot
from telegram.constants import ParseMode
import uvicorn

TOKEN = 'YOUR_BOT_TOKEN'
CHANNEL_ID = '@your_channel_username'
MESSAGE_TEXT = "🔁 This is an automated fixed message."

app = FastAPI()
bot = Bot(token=TOKEN)
last_message_id = None

@app.get("/")
async def root():
    return {"status": "Bot is running."}


async def bot_loop():
    global last_message_id
    while True:
        try:
            if last_message_id:
                await bot.delete_message(chat_id=CHANNEL_ID, message_id=last_message_id)

            sent = await bot.send_message(chat_id=CHANNEL_ID, text=MESSAGE_TEXT, parse_mode=ParseMode.HTML)
            last_message_id = sent.message_id

        except Exception as e:
            print(f"Bot error: {e}")

        await asyncio.sleep(600)  # 10 minutes


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(bot_loop())


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
