"""
Chat room class
"""
from datetime import datetime
from mongoengine import Document, StringField, DateTimeField, ListField


class ChatRoom(Document):
    """
    Chat room object
    """
    creator = StringField(required=True)
    created_at = DateTimeField(required=True, default=datetime.utcnow())
    participants = ListField()

    def __repr__(self):
        return "<Room: %s>" % self.name
