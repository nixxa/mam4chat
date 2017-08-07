''' Chat events '''
from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import SOCKETIO
from ..models import ChatMessage
from .repository import Repository


@SOCKETIO.on('joined', namespace='/chat')
def joined(message):
    """
    Sent by clients when they enter a room.
    A status message is broadcast to all people in the room.
    """
    room = session.get('room')
    actor = session.get('name')
    Repository.get_or_add_room(room, actor)
    Repository.update_user_activity(actor)
    join_room(room)
    last_messages = Repository.get_last(room, actor)
    for item in last_messages:
        emit('message', item.to_json(), room=room)


@SOCKETIO.on('text', namespace='/chat')
def text(message):
    """
    Sent by a client when the user entered a new message.
    The message is sent to all people in the room.
    """
    room = session.get('room')
    msg = message['msg']
    author = session.get('name')
    existing_room = Repository.get_or_add_room(room, author)
    chat_message = ChatMessage(
        room_name=existing_room.name,
        author=author,
        text=msg,
        read_by=[author]
    )
    chat_message.save()
    Repository.update_user_activity(author)
    emit('message', chat_message.to_json(), room=room)


@SOCKETIO.on('left', namespace='/chat')
def left(message):
    """
    Sent by clients when they leave a room.
    A status message is broadcast to all people in the room.
    """
    room = session.get('room')
    actor = session.get('name')
    Repository.logoff(actor)
    leave_room(room)


@SOCKETIO.on('read', namespace='/chat')
def read(message):
    """
    Set status for message
    """
    room = session.get('room')
    actor = session.get('name')
    msg = Repository.get_message(message['id'])
    if not msg is None:
        if not actor in msg.read_by:
            msg.read_by.append(actor)
            msg.save()
    return
