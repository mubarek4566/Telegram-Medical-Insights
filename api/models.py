from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True)
    message_date = Column(DateTime)
    message_text = Column(String)
