from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Any, Type, Optional
from . import db
import random
import string
from website.Models.Room import Room
from .crypto import room_crypto
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
    ciphertext = room_crypto.encrypt_room_code(plaintext)

    room = select_query_function(db.session, Room, Room.room_code == ciphertext)
    if not room:
      print(f"ciphertext: {ciphertext}")
      return ciphertext


# for demo
def get_decrypted_room_code(encrypted_code):
    try:
        return room_crypto.decrypt_room_code(encrypted_code)
    except ValueError:
        return "Invalid Code"