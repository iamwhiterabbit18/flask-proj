from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Any, Type, Optional
from . import db

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