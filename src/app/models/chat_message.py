"""
Chat message class
"""
from datetime import datetime
from mongoengine import Document, StringField, DateTimeField, ListField


class ChatMessage(Document):
    """
    Chat message object
    """
    room_id = StringField(required=True, max_length=100)
    created_at = DateTimeField(default=datetime.utcnow())
    author = StringField(required=True)
    text = StringField(required=True)
    read_by = ListField(StringField())

    def __repr__(self):
        return "<ChatMessage room=%s date=%s, author=%s text=%s>" \
                % (self.room_id, self.created_at, self.author, self.text)
