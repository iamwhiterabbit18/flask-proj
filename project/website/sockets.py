from flask_socketio import SocketIO, emit, join_room, leave_room, send
from flask_login import current_user
from . import socketio, db
from sqlalchemy.orm import Session
from website.Models.Room import Message


@socketio.on('connect')
def handle_connect():
  print(f'Client connected: {current_user.first_name}')

@socketio.on('join')
def handle_join(data):
  print("Join event received")
  print(f"Data: {data}")
  if current_user.is_authenticated:
    room = data.get('room')
    user = data.get('user')
    join_room(room)
    send({"name": room, "message": f"{user} has joined the room"}, to=room)
    print(f'Client connected: {current_user.first_name}')
    print(f'User {user} joined room {room}')
  else:
    print("Unauthenticated user attempted to join.")

@socketio.on('disconnect')
def handle_disconnect():
  print(f'Client disconnected: {current_user.first_name}')


@socketio.on('message')
def handle_message(data):
    room_id = data['room']
    message = data['message']
    print(f"MESSAGE EVENT - Room: {room_id}, User: {current_user.first_name}, Message: {message}")