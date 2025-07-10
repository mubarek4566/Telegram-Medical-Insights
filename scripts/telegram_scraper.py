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
    "Chemed",  # If not found, you may need to use username or invite link
    "https://t.me/lobelia4cosmetics",
    "https://t.me/tikvahpharma"
]

async def scrape_channel(channel_url, limit=1000):
    await client.start(phone=phone_number)
    channel = await client.get_entity(channel_url)
    messages = []
    
    async for msg in client.iter_messages(channel, limit=limit):
        if msg.message or msg.media:
            messages.append({
                "channel": channel.title,
                "message_id": msg.id,
                "text": msg.message,
                "has_media": bool(msg.media),
                "media_type": type(msg.media).__name__ if msg.media else None,
                "date": msg.date.isoformat()
            })

    return messages

async def main():
    all_data = []
    for ch in channels:
        print(f"Scraping: {ch}")
        msgs = await scrape_channel(ch)
        all_data.extend(msgs)

    df = pd.DataFrame(all_data)
    os.makedirs("data/raw", exist_ok=True)
    df.to_json("data/raw/telegram_messages.json", orient="records", lines=True)
    print(f"✅ Saved {len(df)} messages.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
