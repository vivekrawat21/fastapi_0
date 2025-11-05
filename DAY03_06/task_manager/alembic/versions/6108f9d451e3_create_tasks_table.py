"""create tasks table

Revision ID: 6108f9d451e3
Revises: 
Create Date: 2025-11-05 10:43:13.826446

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6108f9d451e3'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create tasks table."""
    # Create enum types first
    op.execute("CREATE TYPE priority AS ENUM ('low', 'medium', 'high')")
    op.execute("CREATE TYPE status AS ENUM ('pending', 'in_progress', 'completed')")
    
    # Create tasks table
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('priority', sa.Enum('low', 'medium', 'high', name='priority'), nullable=True),
        sa.Column('status', sa.Enum('pending', 'in_progress', 'completed', name='status'), nullable=True),
        sa.Column('due_date', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tasks_id'), 'tasks', ['id'], unique=False)


def downgrade() -> None:
    """Drop tasks table and enum types."""
    op.drop_index(op.f('ix_tasks_id'), table_name='tasks')
    op.drop_table('tasks')
    op.execute("DROP TYPE IF EXISTS status")
    op.execute("DROP TYPE IF EXISTS priority")
