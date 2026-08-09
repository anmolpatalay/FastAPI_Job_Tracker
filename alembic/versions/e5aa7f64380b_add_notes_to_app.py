"""add notes to app

Revision ID: e5aa7f64380b
Revises: 4d0073f099b3
Create Date: 2026-08-09 19:10:18.734470

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'e5aa7f64380b'
down_revision: Union[str, Sequence[str], None] = '4d0073f099b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'applications',
        sa.Column('notes', sa.Text(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column('applications', 'notes')