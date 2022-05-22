from datetime import datetime
import sqlalchemy as sa

from .base import Base


class User(Base):
    __tablename__ = 'user'

    id = sa.Column('user_id', sa.Integer, autoincrement=True, primary_key=True)
    created_at = sa.Column(sa.DateTime(timezone=True),
                           nullable=False, default=datetime.utcnow)
    updated_at = sa.Column(sa.DateTime(timezone=True), nullable=False,
                           default=datetime.utcnow, onupdate=datetime.utcnow)
    email = sa.Column(sa.String(64), nullable=False, unique=True)
    username = sa.Column(sa.String(64), nullable=False, unique=True)
    password_hash = sa.Column(sa.String(32), nullable=False)
