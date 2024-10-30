"""second revision

Revision ID: c25acc3c3604
Revises: e82c6da1eef1
Create Date: 2024-10-27 18:23:57.077053

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c25acc3c3604'
down_revision: Union[str, None] = 'e82c6da1eef1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('schedule', sa.Column('date_time', sa.DateTime(), nullable=False))
    op.drop_column('schedule', 'time')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('schedule', sa.Column('time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.drop_column('schedule', 'date_time')
    # ### end Alembic commands ###
