"""add relationship User to Event

Revision ID: 21673b1abcdc
Revises: 6e0eac2a769f
Create Date: 2023-11-15 16:07:12.240752

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '21673b1abcdc'
down_revision: Union[str, None] = '6e0eac2a769f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'events', 'users', ['user_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'events', type_='foreignkey')
    op.drop_column('events', 'user_id')
    # ### end Alembic commands ###
