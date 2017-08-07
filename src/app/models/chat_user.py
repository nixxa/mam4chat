"""
Chat user class
"""
from datetime import datetime
from mongoengine import Document, StringField, DateTimeField, IntField


class ChatUser(Document):
    name = StringField(required=True)
    status = IntField()
    last_seen = DateTimeField(default=datetime.utcnow())
