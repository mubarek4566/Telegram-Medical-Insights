# scripts/telegram_scraper.py

from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime
import json
import logging

# ========================
# ENVIRONMENT SETUP
# ========================
load_dotenv()
api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
phone_number = os.getenv("TELEGRAM_PHONE_NUMBER")

# ========================
# LOGGING CONFIGURATION
# ========================
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("logs/telegram_scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ========================
# TELEGRAM CLIENT SETUP
# ========================
client = TelegramClient("session", api_id, api_hash)
client_started = False

# List of public Telegram channel URLs
channels = [
    "https://t.me/Chemed123",
    "https://t.me/lobelia4cosmetics",
    "https://t.me/tikvahpharma"
]

# ========================
# CONNECT CLIENT
# ========================
async def connect_telegram_client():
    global client_started
    if not client_started:
        logger.info("Connecting to Telegram...")
        await client.start(phone=phone_number)
        client_started = True
        logger.info("Connected to Telegram.")

# ========================
# SCRAPE TELEGRAM MESSAGES
# ========================
async def scrape_telegram_channels(limit=1000):
    await connect_telegram_client()

    today = datetime.today().strftime("%Y-%m-%d")
    base_path = os.path.join("data", "raw", "telegram_messages", today)
    os.makedirs(base_path, exist_ok=True)

    for ch in channels:
        try:
            logger.info(f"Scraping messages from: {ch}")
            channel = await client.get_entity(ch)
            all_data = []

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

            # Save JSON file per channel in partitioned directory
            channel_name = channel.username or channel.title.lower().replace(" ", "_")
            output_file = os.path.join(base_path, f"{channel_name}.json")

            with open(output_file, "w", encoding="utf-8") as f:
                for item in all_data:
                    json.dump(item, f)
                    f.write("\n")

            logger.info(f"Saved {len(all_data)} messages to {output_file}")

        except Exception as e:
            logger.error(f"Error scraping {ch}: {e}")

# ========================
# DOWNLOAD TELEGRAM IMAGES
# ========================
async def download_images_from_channels(save_dir="data/images", limit=1000):
    await connect_telegram_client()

    for ch in channels:
        try:
            logger.info(f"Downloading images from: {ch}")
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
                        logger.warning(f"Error downloading image (msg id: {msg.id}): {e}")

            logger.info(f"Downloaded {count} images from {channel.title} → {output_dir}")
        except Exception as e:
            logger.error(f"Error downloading images from {ch}: {e}")

# ========================
# OPTIONAL: RUN BOTH FROM CLI
# ========================
if __name__ == "__main__":
    import asyncio

    async def run():
        await scrape_telegram_channels()
        await download_images_from_channels()

    asyncio.run(run())
