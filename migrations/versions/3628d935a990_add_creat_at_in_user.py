"""add creat_at in User

Revision ID: 3628d935a990
Revises: d35619815c99
Create Date: 2023-11-15 13:20:46.928459

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3628d935a990'
down_revision: Union[str, None] = 'd35619815c99'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('create', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'create')
    # ### end Alembic commands ###