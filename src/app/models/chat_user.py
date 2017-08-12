"""
Chat user class
"""
from datetime import datetime
from mongoengine import Document, StringField, DateTimeField, IntField


class ChatUser(Document):
    user_id = StringField(required=True)
    status = IntField()
    last_seen = DateTimeField(default=datetime.utcnow())
