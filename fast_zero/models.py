from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func  # type: ignore
from sqlalchemy.orm import (  # type: ignore
    Mapped,
    mapped_column,
    registry,
    relationship,
)

table_registry = registry()


class TodoState(str, Enum):
    draft = 'draft'
    todo = 'todo'
    doing = 'doing'
    done = 'done'
    trash = 'trash'


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    """
    primary_key: diz que o campo será a chave primária da tabela
    unique: diz que o campo só pode ter um valor único em toda a tabela.
    Não podemos ter um username repetido no banco, por exemplo.
    server_default: executa uma função no momento em que
    o objeto for instanciado.

    """

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    todos: Mapped[list['Todo']] = relationship(
        init=False,
        cascade='all, delete-orphan',
        lazy='selectin',
    )


@table_registry.mapped_as_dataclass
class Todo:
    __tablename__ = 'todos'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    state: Mapped[TodoState]

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
