from pydantic import BaseModel
from typing import List
from datetime import datetime, date

class TopProduct(BaseModel):
    has_media: bool
    count: int

class ChannelActivity(BaseModel):
    message_date: date
    messages: int

#class MessageSearchResult(BaseModel):
  #  message_id: str
  #  channel: str
  #  date: date
  #  text: str

class MessageSearchResult(BaseModel):
    message_id: int
    message_date: datetime  
    channel: str
    message_text: str       

    # OR use alias to map external (DB) keys to internal field names
    class Config:
        fields = {
            'message_id': 'message_id',
            'date': 'message_date',
            'text': 'message_text'
        }