from sqlalchemy import Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column

from domain.models.base import Base, BaseModelMixin


class UserModel(Base, BaseModelMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(Text, nullable=False, server_default="")
    password: Mapped[str] = mapped_column(Text, nullable=False, server_default="")
    email: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
