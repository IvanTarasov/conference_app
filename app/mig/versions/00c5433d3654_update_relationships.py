"""update relationships

Revision ID: 00c5433d3654
Revises: c25acc3c3604
Create Date: 2024-10-30 01:35:39.871238

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00c5433d3654'
down_revision: Union[str, None] = 'c25acc3c3604'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
