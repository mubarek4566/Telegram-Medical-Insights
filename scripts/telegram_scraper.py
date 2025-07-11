# scripts/telegram_scraper.py

from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
phone_number = os.getenv("TELEGRAM_PHONE_NUMBER")

client = TelegramClient("session", api_id, api_hash)

channels = [
    "https://t.me/Chemed123",
    "https://t.me/lobelia4cosmetics",
    "https://t.me/tikvahpharma"
]

async def scrape_telegram_channels(limit=1000, save_path="data/raw/telegram_messages.json"):
    await client.start(phone=phone_number)
    all_data = []
    
    for ch in channels:
        print(f"Scraping: {ch}")
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

    df = pd.DataFrame(all_data)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    df.to_json(save_path, orient="records", lines=True)
    print(f"✅ Saved {len(df)} messages to {save_path}")

# Run directly for CLI usage
if __name__ == "__main__":
    import asyncio
    asyncio.run(scrape_telegram_channels())
