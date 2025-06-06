"""create todos table

Revision ID: 149d0ad00858
Revises: 7e2039c30948
Create Date: 2025-05-02 15:22:35.545415

"""
from typing import Sequence, Union

from alembic import op # type: ignore
import sqlalchemy as sa  # type: ignore


# revision identifiers, used by Alembic.
revision: str = '149d0ad00858'
down_revision: Union[str, None] = '7e2039c30948'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todos',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=False),
                    sa.Column('state', sa.Enum('draft', 'todo', 'doing', 'done',
                                               'trash', name='todostate'), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('todos')
    # ### end Alembic commands ###
