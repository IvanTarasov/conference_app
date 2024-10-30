"""downgrade

Revision ID: adcbdddcca13
Revises: 00c5433d3654
Create Date: 2024-10-30 01:49:36.023497

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'adcbdddcca13'
down_revision: Union[str, None] = '00c5433d3654'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
