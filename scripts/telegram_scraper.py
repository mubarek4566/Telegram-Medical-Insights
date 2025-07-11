# scripts/telegram_scraper.py

from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime

# Load credentials
load_dotenv()
api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
phone_number = os.getenv("TELEGRAM_PHONE_NUMBER")

# Telegram session client
client = TelegramClient("session", api_id, api_hash)
client_started = False

# Telegram channel links
channels = [
    "https://t.me/Chemed123",
    "https://t.me/lobelia4cosmetics",
    "https://t.me/tikvahpharma"
]

# Utility function to connect the client once
async def connect_telegram_client():
    global client_started
    if not client_started:
        print("🔌 Connecting to Telegram...")
        await client.start(phone=phone_number)
        client_started = True
        print("✅ Connected to Telegram.")

# Function to scrape messages and save to JSON
async def scrape_telegram_channels(limit=1000, save_path="data/raw/telegram_messages.json"):
    await connect_telegram_client()
    all_data = []

    for ch in channels:
        print(f"🔍 Scraping messages from: {ch}")
        channel = await client.get_entity(ch)
        async for msg in client.iter_messages(channel, limit=limit):
            if msg.message or msg.media:
                all_data.append({
                    "channel": channel.title,
                    "message_id": msg.id,
                    "text": msg.message,
                    "has_media": bool(msg.media),
                    "media_type": type(msg.media).__name__ if msg.media else None,
                    "date": msg.date.isoformat()
                })

    # Save to data lake (JSON)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    pd.DataFrame(all_data).to_json(save_path, orient="records", lines=True)
    print(f"✅ Saved {len(all_data)} messages to {save_path}")

# Function to download images from all channels
async def download_images_from_channels(save_dir="data/images", limit=1000):
    await connect_telegram_client()
    
    for ch in channels:
        print(f"🖼️  Downloading images from: {ch}")
        channel = await client.get_entity(ch)
        folder_name = channel.username or channel.title.lower().replace(" ", "_")
        output_dir = os.path.join(save_dir, folder_name)
        os.makedirs(output_dir, exist_ok=True)

        count = 0
        async for msg in client.iter_messages(channel, limit=limit):
            if msg.media and isinstance(msg.media, MessageMediaPhoto):
                filename = f"{channel.username}_{msg.id}_{datetime.now().timestamp()}.jpg"
                full_path = os.path.join(output_dir, filename)
                try:
                    await client.download_media(msg.media, file=full_path)
                    count += 1
                except Exception as e:
                    print(f"⚠️ Error downloading image: {e}")

        print(f"✅ Downloaded {count} images from {channel.title} → {output_dir}")

# Optional CLI usage
if __name__ == "__main__":
    import asyncio

    async def run():
        await scrape_telegram_channels()
        await download_images_from_channels()

    asyncio.run(run())
