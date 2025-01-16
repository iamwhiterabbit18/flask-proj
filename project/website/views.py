from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import json
from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from .utils import *

from website.Models.Room import Room, RoomParticipant

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
  # Get user's rooms
  with Session(db.engine) as session:
      # stmt = (
      #     select(Room)
      #     .join(RoomParticipant)
      #     .where(RoomParticipant.user_id == current_user.id)
      # )
      # result = session.execute(stmt)
      # user_rooms = result.scalars().all()
      user_rooms = select_joined_query_all_function(session, Room, RoomParticipant.user_id == current_user.id, RoomParticipant)

      # Decrypt room codes for display
      rooms_with_codes = []
      for room in user_rooms:
          room_data = {
              'id': room.id,
              'room_name': room.room_name,
              'plain_code': get_decrypted_room_code(room.room_code)
          }
          rooms_with_codes.append(room_data)

  if request.method == 'POST':
    data = request.form
    form_type = data.get('form_type')
    room_code = data.get('room_code')
    room_name = data.get('room_name')
    room_pass = data.get('room_pass')

    if form_type == 'join_room':
      if not room_code or not room_pass:
        flash('Both room code and password are required.', category='error')
        return redirect(url_for('views.home'))

      # Get all rooms and check if any code matches the input
      with Session(db.engine) as session:
        all_rooms = session.query(Room).all()
        matching_room = None
        for _room in all_rooms:
          try:
            decrypted_code = crypto_manager.decrypt_room_code(_room.room_code)
            if decrypted_code == room_code:
                matching_room = _room
                break
          except ValueError:
              continue
      
      if not matching_room or not check_password_hash(matching_room.password, room_pass):
        flash('Incorrect room code or password', category='error')
        return redirect(url_for('views.home'))
      
      with Session(db.engine) as session:
        condition = and_(
          RoomParticipant.room_id == matching_room.id,
          RoomParticipant.user_id == current_user.id
          )
        room_join = select_query_function(session, RoomParticipant, condition)

      if not room_join:
        new_room_participant = RoomParticipant(room_id=matching_room.id, user_id=current_user.id)
        db.session.add(new_room_participant)
        db.session.commit()
        flash('Joined room!', category='success')
      else:
        flash('Already in room!', category='error')

      return redirect(url_for('views.home'))

    elif form_type == 'create_room':
      if not room_name or not room_pass:
        flash('Both room name and password are required.', category='error')
        return redirect(url_for('views.home'))

      new_room = Room(room_name=room_name, room_code=generate_room_code(), password=generate_password_hash(room_pass, 'pbkdf2:sha256'))
      #debugg
      print(f"New room code: {new_room.room_code}")
      db.session.add(new_room)
      db.session.commit()

      new_room_participant = RoomParticipant(room_id=new_room.id, user_id=current_user.id)
      db.session.add(new_room_participant)
      db.session.commit()

      flash('Room created!', category='success')
      print(f'Creating room: {room_name} {room_pass}')

    else:
      print(f'Unknown form type: {form_type}')
    return redirect(url_for('views.home'))
    
  
  return render_template('home.html', user=current_user, user_rooms=user_rooms, decryptor=get_decrypted_room_code)
# @views.route('/', methods=['GET', 'POST'])
# @login_required
# def home():
#   if request.method == 'POST':
#     note = request.form.get('note')
#     if len(note) < 1:
#       flash('Note is too short!', category='error')
#     else:
#       new_note = Note(data=note, user_id=current_user.id)
#       print(f"Current User: {current_user}\nData: {note}")
#       db.session.add(new_note)
#       db.session.commit()
#       flash('Note added!', category='success')
    
#   return render_template('home.html', user=current_user)

# @views.route('/delete-note', methods=['POST'])
# def delete_note():
#   note = json.loads(request.data)
#   noteId = note['noteId']
#   note = Note.query.get(noteId)
#   if note:
#     if note.user_id == current_user.id:
#       db.session.delete(note)
#       db.session.commit()
    
#   return jsonify({})