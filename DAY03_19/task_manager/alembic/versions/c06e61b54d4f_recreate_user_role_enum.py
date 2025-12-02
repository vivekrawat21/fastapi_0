"""recreate_user_role_enum

Revision ID: c06e61b54d4f
Revises: 8b84a5f32a46
Create Date: 2025-12-02 18:13:48.193368

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c06e61b54d4f'
down_revision: Union[str, Sequence[str], None] = '8b84a5f32a46'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add the role column with correct enum values (uppercase)
    op.add_column('users', sa.Column(
        'role', 
        sa.Enum('ADMIN', 'COLLECTOR', 'SUPERVISOR', name='user_role'),
        nullable=False,
        server_default='COLLECTOR'
    ))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'role')
