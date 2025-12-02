"""fix_user_role_enum_values

Revision ID: 60d241ded889
Revises: 9ad39d401e15
Create Date: 2025-12-02 18:04:10.587046

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '60d241ded889'
down_revision: Union[str, Sequence[str], None] = '9ad39d401e15'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
