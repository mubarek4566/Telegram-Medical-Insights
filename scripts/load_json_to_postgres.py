# scripts/load_raw_json_to_postgres.py

import os
import json
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# PostgreSQL connection details
PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_DB = os.getenv("PG_DB")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")

def connect_db():
    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DB,
        user=PG_USER,
        password=PG_PASSWORD
    )

def create_raw_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE SCHEMA IF NOT EXISTS raw;

            CREATE TABLE IF NOT EXISTS raw.telegram_messages (
                channel TEXT,
                message_id INT,
                text TEXT,
                has_media BOOLEAN,
                media_type TEXT,
                date TIMESTAMP
            );
        """)
        conn.commit()

def load_json_to_postgres(data_dir):
    conn = connect_db()
    create_raw_table(conn)
    inserted_rows = 0

    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                print(f"sLoading: {file_path}")

                with open(file_path, "r", encoding="utf-8") as f:
                    records = [json.loads(line.strip()) for line in f]

                df = pd.DataFrame(records)

                if not df.empty:
                    # Convert DataFrame to Python-native types
                    data_tuples = [
                        (
                            str(row["channel"]),
                            int(row["message_id"]),
                            str(row["text"]) if row["text"] else None,
                            bool(row["has_media"]),
                            str(row["media_type"]) if row["media_type"] else None,
                            pd.to_datetime(row["date"]).to_pydatetime()
                        )
                        for _, row in df.iterrows()
                    ]

                    with conn.cursor() as cur:
                        execute_values(
                            cur,
                            """
                            INSERT INTO raw.telegram_messages (
                                channel, message_id, text,
                                has_media, media_type, date
                            ) VALUES %s
                            """,
                            data_tuples,
                            page_size=100
                        )
                    conn.commit()
                    inserted_rows += len(data_tuples)

    conn.close()
    print(f"✅ Done. Inserted {inserted_rows} rows into raw.telegram_messages.")

# Public function to be called externally (e.g., from Jupyter)
def load_json_data_main(date_str=None):
    """
    Load JSON files from data/raw/telegram_messages/<date> into PostgreSQL.
    If date_str is None, use today's date.
    """
    if not date_str:
        date_str = datetime.today().strftime("%Y-%m-%d")
    data_dir = os.path.join("data", "raw", "telegram_messages", date_str)
    
    if not os.path.exists(data_dir):
        print(f"Directory does not exist: {data_dir}")
        return
    
    load_json_to_postgres(data_dir)

# Optional CLI usage
if __name__ == "__main__":
    load_json_data_main()

def load_image_predictions(csv_path="detections/predictions.csv"):
    conn = connect_db()
    df = pd.read_csv(csv_path)

    # Convert numpy types to native Python types
    df = df.astype({
        "message_id": str,
        "detected_object_class": str,
        "confidence_score": float,
        "channel": str,
        "image_path": str
    })

    # Convert to list of tuples
    data = list(df.itertuples(index=False, name=None))

    with conn.cursor() as cur:
        execute_values(cur, """
            INSERT INTO raw.image_detections (
                message_id, detected_object_class, confidence_score, channel, image_path
            ) VALUES %s
        """, data)
        conn.commit()
        print(f"✅ Loaded {len(df)} detections into raw.image_detections")

    conn.close()