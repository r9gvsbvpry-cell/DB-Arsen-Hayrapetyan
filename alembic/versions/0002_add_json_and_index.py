"""add json field and pg_trgm index

Revision ID: 0002_add_json_and_index
Revises: 0001_initial
Create Date: 2025-12-25
"""
from alembic import op
import sqlalchemy as sa

revision = '0002_add_json_and_index'
down_revision = '0001_initial'
branch_labels = None
dependencies = None


def upgrade():
    # add jsonb column
    op.add_column('assignments', sa.Column('data', sa.dialects.postgresql.JSONB(), nullable=True))
    # create extension and index for regex search using pg_trgm
    op.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm;')
    # gin index on expression
    op.execute("CREATE INDEX IF NOT EXISTS idx_assignments_data_trgm ON assignments USING gin ((data::text) gin_trgm_ops);")


def downgrade():
    op.execute('DROP INDEX IF EXISTS idx_assignments_data_trgm;')
    op.execute('DROP EXTENSION IF EXISTS pg_trgm;')
    op.drop_column('assignments', 'data')
