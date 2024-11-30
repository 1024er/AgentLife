"""
register all socket IO envets in a class.
"""
import os
import json

from utils import (
    find_path, 
    update_grid, 
    generate_random_position
)

CUR_DIR = os.path.dirname(__file__)


def register_events(
    sio,
    rooms,
    items,
    connected_users,
    background_tasks=[]
):
    """
    Custom register events.

    Args:
        sio (_type_): _description_
    """
    @sio.event
    def connect(sid, environ):
        print(f"[Custom Debug Message] User connected: {sid}")
        sio.emit('welcome', {
            'rooms': [{
                'id': room['id'], 
                'name': room['name'], 
                'nbCharacters': len(room['characters'])
            } for room in rooms],
            'items': items
        }, room=sid)
        connected_users.add(sid)

    @sio.event
    def joinRoom(sid, roomId, opts):
        room = next((r for r in rooms if r['id'] == roomId), None)
        
        if not room:
            return
        
        sio.enter_room(sid, room['id'])
        sio.emit(
            'roomJoined', 
            {
                'map': {
                    'gridDivision': room['gridDivision'],
                    'size': room['size'],
                    'items': room['items']
                },
                'characters': room['characters'],
                'id': sid
            }, 
            room=sid
        )
        on_room_update(room)

    def on_room_update(room):
        sio.emit('characters', room['characters'], room=room['id'])
        sio.emit(
            'rooms', 
            [
                {
                    'id': r['id'], 
                    'name': r['name'], 
                    'nbCharacters': len(r['characters'])
                } 
                for r in rooms
            ])

    @sio.event
    def leaveRoom(sid):
        room = next((r for r in rooms if any(c['id'] == sid for c in r['characters'])), None)
        if not room:
            return
        sio.leave_room(sid, room['id'])
        pass

    @sio.event
    def characterAvatarUpdate(sid, avatarUrl):
        room = next((r for r in rooms if any(c['id'] == sid for c in r['characters'])), None)
        if not room:
            return
        character = next(c for c in room['characters'] if c['id'] == sid)
        character['avatarUrl'] = avatarUrl
        sio.emit('characters', room['characters'], room=room['id'])

    @sio.event
    def move(sid, from_pos, to_pos):
        room = next((r for r in rooms if any(c['id'] == sid for c in r['characters'])), None)
        if not room:
            return
        
        character = next(c for c in room['characters'] if c['id'] == sid)
        path, path_len = find_path(room, from_pos, to_pos)
        if not path:
            return
        
        character['position'] = from_pos
        character['path'] = path

        character_serializable = {
            'id': character['id'],
            'session': character['session'],
            'position': character['position'],
            'path': [(node.x, node.y) for node in character['path']],
            'avatarUrl': character['avatarUrl']
        }

        sio.emit('playerMove', character_serializable, room=room['id'])

    @sio.event
    def dance(sid):
        sio.emit('playerDance', {'id': sid}, room=sid)

    @sio.event
    def chatMessage(sid, message):
        room = next((r for r in rooms if any(c['id'] == sid for c in r['characters'])), None)
        if not room:
            return
        sio.emit('playerChatMessage', {'id': sid, 'message': message}, room=room['id'])

    @sio.event
    def passwordCheck(sid, password):
        room = rooms[0]
        if password == room['password']:
            sio.emit('passwordCheckSuccess')
        else:
            sio.emit('passwordCheckFail')

    @sio.event
    def itemsUpdate(sid, items):
        room = rooms[0]
        room['items'] = items
        update_grid(room)
        
        for character in room['characters']:
            character['path'] = []
            character['position'] = generate_random_position(room)
        
        sio.emit('mapUpdate', {
            'map': {
                'gridDivision': room['gridDivision'],
                'size': room['size'],
                'items': room['items']
            },
            'characters': room['characters']
        }, room=room['id'])
        
        try:
            rooms_serializable = [{k: v for k, v in room.items() if k != 'grid'} for room in rooms]
            newest_rooms_json = os.path.join(CUR_DIR, 'configs', 'newest_rooms.json')
            with open(newest_rooms_json, 'w') as f:
                json.dump(rooms_serializable, f, indent=2, ensure_ascii=False)
            print(f"Rooms data has saved to {newest_rooms_json}.")
        except TypeError as e:
            print(f"Error serializing rooms: {e}")
            print("Rooms data:", rooms)
            raise

    @sio.event
    def disconnect(sid):
        print("User disconnected")
        # room = next((r for r in rooms if any(c['id'] == sid for c in r['characters'])), None)
        # if room:
        #     room['characters'] = [c for c in room['characters'] if c['id'] != sid]
            # on_room_update(room)
        connected_users.remove(sid)
            
    if background_tasks:
        for background_task in background_tasks:
            sio.start_background_task(background_task)