from flask_socketio import SocketIO, emit, join_room, leave_room, send
from flask_login import current_user
from . import socketio, db
from sqlalchemy.orm import Session
from website.Models.Room import Message


def init_socket_handlers(socketio):
    @socketio.on('connect')
    def handle_connect():
        if current_user.is_authenticated:
            print(f'Client connected: {current_user.first_name}')
        else:
            print('Anonymous client connected')

    @socketio.on('join')
    def handle_join(data):
        if current_user.is_authenticated:
            room = data.get('room')
            user = data.get('user')
            if room and user:
                join_room(room)
                emit('status', {'message': f'{user} has joined the room'}, to=room)
                print(f'User {user} joined room {room}')
        else:
            print("Unauthenticated user attempted to join.")

    @socketio.on('disconnect')
    def handle_disconnect():
        if current_user.is_authenticated:
            print(f'Client disconnected: {current_user.first_name}')
        else:
            print('Anonymous client disconnected')

    @socketio.on('message')
    def handle_message(data):
        if current_user.is_authenticated:
            room_id = data.get('room')
            message = data.get('message')
            if room_id and message:
                print(f"MESSAGE EVENT - Room: {room_id}, User: {current_user.first_name}, Message: {message}")
                new_message = Message(room_id=room_id, user_id=current_user.id, message=message)
                db.session.add(new_message)
                db.session.commit()
                emit('message', {
                    'room': room_id,
                    'user': current_user.first_name,
                    'message': message
                }, room=room_id)