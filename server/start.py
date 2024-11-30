"""
Main world class, which calculate every state of the world,
and emit events to the clients.
"""
import os

from gevent import monkey
monkey.patch_all()

import eventlet
import socketio
from flask import Flask

from agent import Agent
from socket_helper import register_events
from utils import load_rooms, load_items


class World(object):

    origin = os.getenv('CLIENT_URL', 'http://localhost:5173')
    sio = socketio.Server(
        cors_allowed_origins=origin
    )
    app = Flask(__name__)
    app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)
    print(f"Server started, allowed cors origin: {origin}")
    
    def __init__(self):
        """
        Init func.
        
        Args:
            sio: socket IO, used to emit events.
        """
        self.connected_users = set()
        self.items = load_items()
        self.rooms = load_rooms()
        self.agents = [
            Agent(
                world=self,
                character=character, 
                sio=self.sio,
                room=room
            ) for room in self.rooms for character in room['characters']
        ]
        all_background_tasks = [
            agent.main_loop for agent in self.agents
        ]
        register_events(
            self.sio, 
            self.rooms, 
            self.items,
            self.connected_users,
            background_tasks=all_background_tasks
        )
    
    def start_server(
        self,
        listen_port=3000
    ):
        """
        Start the server.
        """
        eventlet.wsgi.server(
            eventlet.listen(('', listen_port)), 
            self.app
        )
        
            
if __name__ == '__main__':
    world = World()
    world.start_server()