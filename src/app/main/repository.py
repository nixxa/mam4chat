"""
Class and method for working with database models
"""
from datetime import datetime
from ..models import ChatRoom, ChatMessage, ChatUser

class Repository:
    """
    Repository for rooms and messages
    """
    @staticmethod
    def get_or_add_room(room, actor):
        """
        Get or add room
        """
        existing_room = ChatRoom.objects(name=room).first()
        if existing_room is None:
            chat_room = ChatRoom(
                name=room,
                creator=actor,
                participants=[actor])
            chat_room.save()
        else:
            if not actor in existing_room.participants:
                existing_room.participants.append(actor)
                existing_room.save()
        return existing_room


    @staticmethod
    def get_message(msg_id):
        msg = ChatMessage.objects.get(id=msg_id)
        return msg


    @staticmethod
    def update_user_activity(actor):
        user = ChatUser.objects(name=actor).first()
        if user is None:
            user = ChatUser(
                name=actor,
                status=1
            )
            user.save()
        else:
            user.last_seen = datetime.utcnow()
            user.save()
        return user

    
    @staticmethod
    def logoff(actor):
        user = ChatUser.objects(name=actor).first()
        if user is None:
            user = ChatUser(
                name=actor,
                status=0
            )
            user.save()
        else:
            user.last_seen = datetime.utcnow()
            user.status = 0
            user.save()
        return user


    @staticmethod
    def get_last(room, actor):
        messages = ChatMessage.objects(room_name=room)
        return messages
