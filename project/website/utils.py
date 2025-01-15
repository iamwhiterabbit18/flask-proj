from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Any, Type, Optional
from . import db
import random
import string
from website.Models.Room import Room, Message
from .crypto import crypto_manager
from werkzeug.security import generate_password_hash

# sql query function
def select_query_function(session: Session, target: Type, filter_condition: Any) -> Optional[Any]:
  try:
    stmt = (
      select(target)
      .where(filter_condition)
    )
    result = session.execute(stmt)
    return result.scalars().one_or_none()
  except Exception as e:
    print(f"Error executing select query: {e}")
    return None

def select_joined_query_function(session: Session, target: Type, filter_condition: Any, joined: Type) -> Optional[Any]:
  try:
    stmt = (
      select(target)
      .join(joined)
      .where(filter_condition)
    )
    result = session.execute(stmt)
    return result.scalars().one_or_none()
  except Exception as e:
    print(f"Error executing joined select query: {e}")
    return None

def select_joined_query_all_function(session: Session, target: Type, filter_condition: Any, joined: Type) -> Optional[Any]:
  try:
    stmt = (
      select(target)
      .join(joined)
      .where(filter_condition)
    )
    result = session.execute(stmt)
    return result.scalars().all()
  except Exception as e:
    print(f"Error executing joined select query: {e}")
    return None


# generate room code
def generate_room_code():
  while True:
    plaintext = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    ciphertext = crypto_manager.encrypt_room_code(plaintext)

    room = select_query_function(db.session, Room, Room.room_code == ciphertext)
    if not room:
      print(f"ciphertext: {ciphertext}")
      return ciphertext

def get_decrypted_room_code(encrypted_code):
    try:
        return crypto_manager.decrypt_room_code(encrypted_code)
    except ValueError:
        return "Invalid Code"

# messages

def save_message(user_id: int, room_id: int, message_content: str) -> Message:
    """Save an encrypted message"""
    try:
        # Encrypt the message content
        encrypted_content = crypto_manager.encrypt_message(message_content)
        
        # Create new message
        new_message = Message(
            message=encrypted_content,
            user_id=user_id,
            room_id=room_id
        )
        
        db.session.add(new_message)
        db.session.commit()
        return new_message
    except Exception as e:
        db.session.rollback()
        raise e

def get_decrypted_message(message: Message) -> str:
    """Get decrypted content of a message"""
    try:
        return crypto_manager.decrypt_message(message.message)
    except ValueError:
        return "Message decryption failed"

def get_room_messages(room_id: int, limit: int = 50) -> list:
    """Get recent messages for a room with decrypted content"""
    messages = Message.query.filter_by(room_id=room_id)\
        .order_by(Message.created_at.desc())\
        .limit(limit)\
        .all()
    
    decrypted_messages = []
    for msg in messages:
        decrypted_messages.append({
            'id': msg.id,
            'content': get_decrypted_message(msg),
            'timestamp': msg.created_at,
            'user_id': msg.user_id
        })
    
    return decrypted_messages[::-1]  # Reverse to get chronological order