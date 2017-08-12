''' Chat events '''
#pylint: disable=E1101
import json

from datetime import datetime

from flask import g, request
from flask_socketio import emit, join_room, leave_room
from werkzeug.utils import escape

from .. import SOCKETIO
from ..models import ChatMessage, ChatRoom, ChatUser
from .api import verify_token


@SOCKETIO.on('join', namespace='/chat')
def join(room_id):
    """
    Joining user to the room
    """
    token = request.args["token"]
    token_valid = verify_token(token)
    if not token_valid:
        return
    current_user_id = str(g.current_user)
    join_room(room_id)
    conversation = ChatRoom.objects().get(id=room_id)
    if not conversation is None:
        if not current_user_id in conversation.participants:
            conversation.participants.append(current_user_id)
            conversation.save()
    emit("joined", conversation.to_json())


@SOCKETIO.on('leave', namespace='/chat')
def leave(room_id):
    """
    Leave the specified room
    """
    token = request.args["token"]
    token_valid = verify_token(token)
    if not token_valid:
        return
    leave_room(room_id)


@SOCKETIO.on('text', namespace='/chat')
def text(message):
    """
    Sent by a client when the user entered a new message.
    The message is sent to all people in the room.
    """
    token = request.args["token"]
    token_valid = verify_token(token)
    if not token_valid:
        return
    conversation_id = message["conversation"]
    txt = message["text"]
    if txt == "":
        return
    author_id = str(g.current_user)
    conversation = ChatRoom.objects().get(id=conversation_id)
    if not conversation:
        return
    chat_message = ChatMessage(
        room_id=conversation_id,
        created_at=datetime.utcnow(),
        author=author_id,
        text=escape(txt),
        read_by=[author_id]
    )
    chat_message.save()
    update_user_activity(author_id)
    emit('message', chat_message.to_json(), room=conversation_id)


@SOCKETIO.on('read', namespace='/chat')
def read(message):
    """
    Set status for message
    """
    token = request.args["token"]
    token_valid = verify_token(token)
    if not token_valid:
        return
    conversation_id = message["conversation"]
    message_id = message["messageId"]
    author_id = str(g.current_user)
    msg = ChatMessage.objects().get(id=message_id)
    if not msg is None:
        if not author_id in msg.read_by:
            msg.read_by.append(author_id)
            msg.save()
            emit('read', msg.to_json(), room=conversation_id)
    return


@SOCKETIO.on('typing', namespace='/chat')
def typing(message):
    """
    Set user status to typing
    """
    token = request.args["token"]
    token_valid = verify_token(token)
    if not token_valid:
        return
    conversation_id = message["conversation"]
    author_id = str(g.current_user)
    author = ChatUser.objects(user_id=author_id).first()
    emit('typing', {"user": json.loads(author.to_json()), "typing": True}, room=conversation_id)


def update_user_activity(uid):
    """
    Update user status and date of last activity
    :param: uid - user identity
    """
    user = ChatUser.objects(user_id=uid).first()
    if user is None:
        user = ChatUser(
            user_id=uid,
            status=1
        )
        user.save()
    else:
        user.last_seen = datetime.utcnow()
        user.save()
    return user
