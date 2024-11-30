"""
utils functions.
"""
import os
import json
import math
import random
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


CUR_DIR = os.path.dirname(__file__)

finder = AStarFinder(
    diagonal_movement=True
)

ROOMS, ITEMS = [], []


def find_path(
    room, 
    start: list, 
    end: list
) -> list:
    """
    find path from start to end in a grid matrix.

    Args:
        room (_type_): _description_
        start (_type_): _description_
        end (_type_): _description_

    Returns:
        path (list): path from start to end, e.g. -> [(0, 0), (0, 1), (0, 2), (1, 2)]
    """
    start = room['grid'].node(start[0], start[1])
    end = room['grid'].node(end[0], end[1])
    path = finder.find_path(
        start,
        end,
        room['grid']
    )
    return path


def update_grid(room):
    """
    update grid matrix with items, often called when items are updated.

    Args:
        room (_type_): _description_
    """
    for x in range(room['size'][0] * room['gridDivision']):
        for y in range(room['size'][1] * room['gridDivision']):
            room['grid'].node(x, y).walkable = True

    for item in room['items']:
        if item.get('walkable') or item.get('wall'):
            continue
        
        width = item['size'][1] if item.get('rotation') in [1, 3] else item['size'][0]
        height = item['size'][0] if item.get('rotation') in [1, 3] else item['size'][1]
        for x in range(width):
            for y in range(height):
                room['grid'].node(item['gridPosition'][0] + x, item['gridPosition'][1] + y).walkable = False


def generate_random_position(room):
    """
    generate a random valid position in the room, which can not collide with items.

    Args:
        room (_type_): _description_

    Returns:
        _type_: _description_
    """
    for _ in range(100):
        x = random.randint(0, room['size'][0] * room['gridDivision'] - 1)
        y = random.randint(0, room['size'][1] * room['gridDivision'] - 1)
        if room['grid'].node(x, y).walkable:
            return [x, y]


def load_rooms():
    """
    Load rooms from local json file.
    """
    global ROOMS
    
    if not ROOMS:
        rooms = []
        
        try:
            with open(os.path.join(CUR_DIR, 'configs', 'newest_rooms.json'), 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print("No rooms.json file found, using default file")
            try:
                with open('configs/default_rooms.json', 'r') as f:
                    data = json.load(f)
            except FileNotFoundError:
                print("No default.json file found, exiting")
                exit(1)
        
        for room_item in data:
            room = room_item.copy()
            room['grid'] = Grid(matrix=[[1] * (room['size'][0] * room['gridDivision']) for _ in range(room['size'][1] * room['gridDivision'])])
            update_grid(room)
            
            for chracter in room['characters']:
                chracter['position'] = generate_random_position(room)
            
            rooms.append(room)
        
        ROOMS = rooms
        return rooms
    else:
        return ROOMS
    

def load_items():
    """
    Load items from local json file.
    """
    global ITEMS
    
    if not ITEMS:
        items_path = os.path.join(CUR_DIR, 'configs', 'shop_items.json')
        with open(items_path, 'r') as f:
            items = json.load(f)
        ITEMS = items
        return items
    else:
        return ITEMS


def get_item_position(
    items: list, 
    target_item: str
) -> list:
    """Get item position in grid matrix.

    Args:
        item (_type_): _description_

    Returns:
        _type_: _description_
    """
    for item in items:
        if item['name'] == target_item:
            return {
                "gridPosition": item['gridPosition'],
                "entryGridPosition": item.get('entryGridPosition', None),
                "entryLookAt": item.get('entryLookAt', None),
            }
    return None
        

def distance(
    point1: list,
    point2: list
):
    """Calculate distance between two points.

    Args:
        point1 (list): _description_
        point2 (list): _description_
    """
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)