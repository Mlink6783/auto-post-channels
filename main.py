import asyncio
import os
from pyrogram import Client, filters
from flask import Flask
from threading import Thread

# Render Environment Variables
API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
BOT_USERNAME = os.environ.get('BOT_USERNAME', 'DatingBotUsername') 
SESSION_STRING = os.environ.get('SESSION_STRING')

if SESSION_STRING:
    app = Client("my_bot", session_string=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)
else:
    app = Client("my_account", api_id=API_ID, api_hash=API_HASH)

# common promo text (Dating bot o private chat-er jonno same)
promo_text = (
    "Girls and boys zone 18+ only.. 100% Free random video chats , 1v1 chats\n\n"
    "Daily Gender wise 50 times free sarch\n\n"
    "only real telegrm users\n\n"
    "just take a look : https://t.co/rh8nCe5WGl"
)

promo_text1 = (
   " Thanks , please wait ... "
)

# Protiti user-ke ekbar reply dewar jonno list
replied_users = set()

# Private Chat Handler (Sudhu inbox-er jonno)
@app.on_message(filters.private & ~filters.bot)
async def auto_reply(client, message):
    # Dating bot chara onno keu message dile ebong jodi age reply na peye thake
    if message.chat.username != BOT_USERNAME and message.from_user.id not in replied_users:
        try:
            await message.reply_text(promo_text1)
            replied_users.add(message.from_user.id)
            print(f"Auto-reply sent to: {message.from_user.id}")
        except Exception as e:
            print(f"Reply error: {e}")

# Render-er jonno web server
web = Flask('')

@web.route('/')
def home():
    return "Bot is running 24/7!"

async def automation():
    async with app:
        print("--- Automation & Private Reply Started ---")
        while True:
            try:
                # ১. সার্চ কমান্ড পাঠানো (Ager motoi same)
                await app.send_message(BOT_USERNAME, "🙍‍♂️ Find a guy")
                print("Searching...")
                await asyncio.sleep(4) 

                # ২. Dating bot-e promo text pathano (Ager motoi same)
                await app.send_message(BOT_USERNAME, promo_text)
                await asyncio.sleep(3)

                please_text = "plz join so that we both get 50 free gender wise match limit"
                await app.send_message(BOT_USERNAME, please_text)
                print("Messages sent to Dating Bot!")
                await asyncio.sleep(3)

                # ৩. স্টপ পাঠানো
                await app.send_message(BOT_USERNAME, "/stop")
                print("Cycle complete. Sleeping...")
                
                # ৪. বিরতি
                await asyncio.sleep(3) 

            except Exception as e:
                print(f"Error encountered: {e}")
                await asyncio.sleep(5)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    
    # Web server thread-e chalao
    Thread(target=lambda: web.run(host='0.0.0.0', port=port, use_reloader=False)).start()
    
    # App run kora (Automation ebong Auto-reply eksathe kaj korbe)
    app.run(automation())
