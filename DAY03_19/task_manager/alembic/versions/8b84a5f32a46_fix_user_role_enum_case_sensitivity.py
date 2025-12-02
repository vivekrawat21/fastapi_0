"""fix_user_role_enum_case_sensitivity

Revision ID: 8b84a5f32a46
Revises: 60d241ded889
Create Date: 2025-12-02 18:04:22.667520

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b84a5f32a46'
down_revision: Union[str, Sequence[str], None] = '60d241ded889'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop the existing role column
    op.drop_column('users', 'role')

    # Recreate the role column with correct enum values (uppercase)
    op.add_column('users', sa.Column('role', sa.Enum('ADMIN', 'COLLECTOR', 'SUPERVISOR', name='user_role'), nullable=False, server_default='COLLECTOR'))


def downgrade() -> None:
    """Downgrade schema."""
    # Drop the role column
    op.drop_column('users', 'role')
