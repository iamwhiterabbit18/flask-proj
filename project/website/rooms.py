from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import json
from sqlalchemy import select
from sqlalchemy.orm import Session

from website.Models.Room import Room, RoomParticipant, Message

from .utils import *

rooms = Blueprint('rooms', __name__)

@rooms.route('/room/<room_id>', methods=['GET', 'POST'])
@login_required
def room_handler(room_id):

    #check if room is existing
    with Session(db.engine) as session:
      room = select_query_function(session, Room, Room.id == room_id)

    if not room:
      flash(f"Room {room_id} does not exist.", category='error')
      response = redirect(url_for('views.home'))
      return response

    if request.method == 'GET':
      # check if current user belongs to the room
      with Session(db.engine) as session:
        room_participant = select_joined_query_function(session, current_user, current_user.id == RoomParticipant.user_id, RoomParticipant)
      
      # query all messages
      with Session(db.engine) as session:
        messages = select_joined_query_all_function(session, Message, Message.room_id == room_id, Message)

      if not room_participant:
        print(f"You don't belong to the room. Try ask for access credentials.")
      
      # print(f"Room page{room_id}\nRoom: {room}\nRoom Participant: {current_user.first_name}")
      return render_template('room.html', room=room, user=current_user, messages=messages)

    # Render room-specific page
    return render_template('room.html', room=room)