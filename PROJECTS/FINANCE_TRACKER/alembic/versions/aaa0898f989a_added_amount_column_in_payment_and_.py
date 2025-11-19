"""added amount column in Payment and removed unecessary enums from the transactions

Revision ID: aaa0898f989a
Revises: 52409e761993
Create Date: 2025-11-18 17:03:31.377255

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aaa0898f989a'
down_revision: Union[str, None] = '52409e761993'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
