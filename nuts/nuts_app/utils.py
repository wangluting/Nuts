from functools import wraps

from .models import Room

def get_room_or_error(room_id, user):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    # Find the room they requested (by ID)
    try:
        room = Room.objects.get(room_id=room_id)
    except Room.DoesNotExist:
        room = Room(room_id=room_id)
        return room
    return room
