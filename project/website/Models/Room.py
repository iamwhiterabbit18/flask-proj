from website import db
from sqlalchemy.sql import func

class Room(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  room_name = db.Column(db.String(255), nullable=False)
  room_code = db.Column(db.String(512), nullable=False)
  password = db.Column(db.String(255), nullable=False)
  created_at = db.Column(db.DateTime(timezone=True), default=func.now())

class RoomParticipant(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  created_at = db.Column(db.DateTime(timezone=True), default=func.now())

class Message(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  message = db.Column(db.Text, nullable=False)
  created_at = db.Column(db.DateTime(timezone=True), default=func.now())