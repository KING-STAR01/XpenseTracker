
from sqlalchemy import String, Integer, Float, ForeignKey, FetchedValue
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import func
from datetime import datetime
from typing import List, Optional
# from sqlalchemy.schema import FetchedValue


class Base(DeclarativeBase):
    pass

"""
{'update_id': 815454850,
'message': {'message_id': 155,
'from': {'id': 1314612220, 'is_bot': False, 'first_name': 'KINGSTAR', 'username': 'KING_STAR_0', 'language_code': 'en'},
'chat': {'id': 1314612220, 'first_name': 'KINGSTAR', 'username': 'KING_STAR_0', 'type': 'private'},
 'date': 1704381532, 'text': 'Hi'}}
"""


class User(Base):
    __tablename__ = 'user_model'

    username: Mapped[str] = mapped_column(String(50), primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    expense: Mapped[List["Expense"]] = relationship("Expense", back_populates="user")

class Expense(Base):
    __tablename__ = "expense_model"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    category: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(String(256), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    username: Mapped[str] = mapped_column(String(50), ForeignKey('user_model.username'))  # new line

    # updated_at: Mapped[datetime] = mapped_column(
    #     server_default=FetchedValue(), server_onupdate=FetchedValue()
    # )
    user: Mapped[User] = relationship("User", back_populates="expense")
