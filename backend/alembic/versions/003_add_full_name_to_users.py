"""add full_name to users

Revision ID: 003
Revises: 002
Create Date: 2026-02-18
"""
from alembic import op
import sqlalchemy as sa

revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('full_name', sa.String(255), nullable=True))


def downgrade():
    op.drop_column('users', 'full_name')
