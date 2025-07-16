from fastapi import FastAPI
from typing import List
from .schemas import TopProduct, ChannelActivity, MessageSearchResult
from .crud import get_top_products, get_channel_activity, search_messages

app = FastAPI(title="Telegram Medical Insights API")

@app.get("/api/reports/top-products", response_model=List[TopProduct])
def top_products(limit: int = 10):
    return get_top_products(limit=limit)

@app.get("/api/channels/{channel_id}/activity", response_model=list[ChannelActivity])
def channel_activity(channel_id: str):
    return get_channel_activity(channel_id)

@app.get("/api/search/messages", response_model=List[MessageSearchResult])
def search(query: str, limit: int = 10):
    return search_messages(query=query, limit=limit)
