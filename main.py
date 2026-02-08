import asyncio
import os
from pyrogram import Client
from flask import Flask
from threading import Thread

# Render Environment Variables থেকে ডেটা সংগ্রহ
API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
BOT_USERNAME = os.environ.get('BOT_USERNAME', 'DatingBotUsername') # ডিফল্ট ইউজারনেম দিতে পারেন

# সেশন স্ট্রিং পদ্ধতি (Render-এর জন্য সবথেকে ভালো)
SESSION_STRING = os.environ.get('SESSION_STRING')

if SESSION_STRING:
    app = Client("my_bot", session_string=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)
else:
    # যদি সেশন স্ট্রিং না থাকে তবে লোকাল ফাইল ব্যবহার করবে
    app = Client("my_account", api_id=API_ID, api_hash=API_HASH)

# Render-এর জন্য ওয়েব সার্ভার
web = Flask('')

@web.route('/')
def home():
    return "Bot is running 24/7!"

def run_web():
    web.run(host='0.0.0.0', port=8080)

async def automation():
    async with app:
        print("--- Automation Started ---")
        while True:
            try:
                # ১. /search পাঠানো
                await app.send_message(BOT_USERNAME, "/search")
                print("Searching...")
                await asyncio.sleep(6) # একটু বেশি সময় দেওয়া নিরাপদ

                # ২. মেসেজ পাঠানো (র‍্যান্ডম বিরতি সহ)
                promo_text = "Girls and boys zone 18+ only.. 100% Free just take a look 👉 : https://t.co/rh8nCe5WGl"
                await app.send_message(BOT_USERNAME, promo_text)
                await asyncio.sleep(7)

                please_text = "plz join so that we both get 50 free gender wise match limit"
                await app.send_message(BOT_USERNAME, please_text)
                print("Messages sent!")
                await asyncio.sleep(7)

                # ৩. /stop পাঠানো
                await app.send_message(BOT_USERNAME, "/stop")
                print("Cycle complete. Sleeping...")
                
                # ৪. বড় বিরতি (অ্যাকাউন্ট সেফ রাখার জন্য কমপক্ষে ৬০-৯০ সেকেন্ড দিন)
                await asyncio.sleep(10) 

            except Exception as e:
                print(f"Error encountered: {e}")
                await asyncio.sleep(5)

if __name__ == "__main__":
    # Render এর জন্য পোর্ট ম্যানেজমেন্ট
    port = int(os.environ.get("PORT", 8080))
    
    # ওয়েব সার্ভার আলাদা থ্রেডে চালানো
    Thread(target=lambda: web.run(host='0.0.0.0', port=port, use_reloader=False)).start()
    
    # অটোমেশন শুরু
    app.run(automation())
