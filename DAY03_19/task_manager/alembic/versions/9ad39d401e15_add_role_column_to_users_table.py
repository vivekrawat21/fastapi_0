"""add_role_column_to_users_table

Revision ID: 9ad39d401e15
Revises: 72e43155c310
Create Date: 2025-12-02 17:54:50.512102

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ad39d401e15'
down_revision: Union[str, Sequence[str], None] = '72e43155c310'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add role column to users table with default value 'Collector'
    op.add_column('users', sa.Column('role', sa.Enum('Admin', 'Collector', 'Supervisor', name='user_role'), nullable=False, server_default='Collector'))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove role column from users table
    op.drop_column('users', 'role')
