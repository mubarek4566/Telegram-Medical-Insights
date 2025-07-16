from .database import connect_db

def get_top_products(limit: int):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT has_media, COUNT(*) AS count
        FROM analytics.fct_messages
        GROUP BY has_media
        ORDER BY count DESC
        LIMIT %s;
    """, (limit,))
    result = cur.fetchall()
    cur.close()
    conn.close()
    return [{"has_media": row[0], "count": row[1]} for row in result]

def get_channel_activity(channel_id: str):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT message_date, COUNT(*) AS messages
        FROM analytics.fct_messages
        WHERE channel_id = %s
        GROUP BY message_date
        ORDER BY message_date
    """, (channel_id,))
    
    data = [{"message_date": row[0], "messages": row[1]} for row in cur.fetchall()]
    
    cur.close()
    conn.close()
    return data

def search_messages(query: str, limit=10):
    conn = connect_db()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT message_id, channel, message_date, message_text
            FROM analytics.stg_telegram_messages
            WHERE message_text ILIKE %s
            ORDER BY message_date DESC
            LIMIT %s
        """, (f"%{query}%", limit))
        rows = cur.fetchall()
    conn.close()
    return [
        {"message_id": r[0], "channel": r[1], "message_date": r[2], "message_text": r[3]}
        for r in rows
    ]

