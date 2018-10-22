from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import DATETIME, INTEGER, TEXT, BOOLEAN
import datetime
Base = declarative_base()

class Event(Base):
    __tablename__ = 'event'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(INTEGER, primary_key=True, nullable=False)
    name = Column(TEXT)
    server = Column(TEXT)
    date = Column(DATETIME)


class Attendance(Base):
    __tablename__ = 'attendance'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(INTEGER, primary_key=True, nullable=False)
    member_id = Column(TEXT)
    event_id = Column(TEXT)


class Member(Base):
    __tablename__ = 'member'
    id = Column(INTEGER, primary_key=True, nullable=False)
    name = Column(TEXT)
    avatar = Column(TEXT)
    level = Column(INTEGER)
    experience = Column(INTEGER)

class Command(Base):
    __tablename__ = 'command'
    name = Column(TEXT, primary_key=True, nullable=False)
    description = Column(TEXT)
    content = Column(TEXT)

class Token(Base):
    __tablename__ = 'token'
    date = Column(DATETIME, primary_key=True, nullable=False)
    price = Column(INTEGER)


class User(Base):
    __tablename__ = "users"
    id = Column(INTEGER, primary_key=True)
    email = Column(TEXT, unique=True, nullable=False)
    name = Column(TEXT, nullable=True)
    avatar = Column(TEXT)
    active = Column(BOOLEAN, default=False)
    tokens = Column(TEXT)
    created_at = Column(DATETIME, default=datetime.datetime.utcnow())