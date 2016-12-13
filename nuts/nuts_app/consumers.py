from django.http import HttpResponse
from channels.handler import AsgiHandler

from channels import Group
from channels.sessions import channel_session

import json
from channels import Channel
from channels.auth import channel_session_user_from_http, channel_session_user

from models import Room
from .utils import get_room_or_error


@channel_session_user_from_http
def ws_connect(message):
    # Initialise session
    message.channel_session['rooms'] = []


# read as json
def ws_receive(message):
    payload = json.loads(message['text'])
    payload['reply_channel'] = message.content['reply_channel']
    Channel("chat.receive").send(payload)


@channel_session_user
def ws_disconnect(message):
    for room_id in message.channel_session.get("rooms", set()):
        try:
            room = Room.objects.get(room_id=room_id)
            room.websocket_group.discard(message.reply_channel)
        except Room.DoesNotExist:
            pass


@channel_session_user
def chat_join(message):
    # get the room or create one
    room = get_room_or_error(message["room"], message.user)

    room.websocket_group.add(message.reply_channel)
    message.channel_session['rooms'] = list(set(message.channel_session['rooms']).union([room.room_id]))


@channel_session_user
def chat_leave(message):
    room = get_room_or_error(message["room"], message.user)

    room.websocket_group.discard(message.reply_channel)
    message.channel_session['rooms'] = list(set(message.channel_session['rooms']).difference([room.id]))


@channel_session_user
def chat_send(message):
    room = get_room_or_error(message["room"], message.user)
    room.send_message(message["message"], message.user)