"""
API for chat
"""
#pylint: disable=E1101
import logging
import json

from flask import (current_app, g, request)
from flask_httpauth import HTTPTokenAuth
from flask_jwt import jwt

from . import main
from ..models import ChatMessage, ChatRoom


LOGGER = logging.getLogger(__name__)
AUTH = HTTPTokenAuth(scheme='Bearer')


@AUTH.verify_token
def verify_token(token):
    """
    Token verification
    :param token: authorization token
    """
    decoded = jwt.decode(token, current_app.config["SECRET_KEY"], verify=True)
    current_user_id = decoded['identity']
    if not current_user_id is None:
        g.current_user = current_user_id
        return True
    return False


@main.route("/api/conversations", methods=["GET"])
@AUTH.login_required
def conversations():
    """
    Return list of conversations for current user
    """
    current_user_id = g.current_user
    rooms = ChatRoom.objects(participants=str(current_user_id))
    return rooms.to_json()


@main.route("/api/start", methods=["POST"])
@AUTH.login_required
def start_conversation():
    """
    Starting new conversation with specified members
    """
    current_user_id = g.current_user
    message = request.json
    members = [str(current_user_id)]
    if isinstance(message["participants"], list):
        for item in message["participants"]:
            members.append(str(item))
    else:
        members.append(str(message["participants"]))
    existing = ChatRoom.objects(participants=members).first()
    if existing is None:
        existing = ChatRoom(
            creator=str(current_user_id),
            participants=members
        )
        existing.save()
    else:
        if not current_user_id in existing.participants:
            existing.participants.append(str(current_user_id))
            existing.save()
    return existing.to_json()


@main.route("/api/history/<room>")
@AUTH.login_required
def history(room):
    """
    Returns room history (last 10 messages)
    :param room: conversation identifier
    """
    existing = ChatRoom.objects.get(id=room)
    if existing is None:
        return 404, 'No room with id='+room
    messages = ChatMessage.objects(room_id=room).order_by("-created_at")[:10]
    return messages.to_json()
