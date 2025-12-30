"""initial

Revision ID: 0001_initial
Revises: 
Create Date: 2025-12-25
"""
from alembic import op
import sqlalchemy as sa

revision = '0001_initial'
down_revision = None
branch_labels = None
dependencies = None


def upgrade():
    op.create_table('projects',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('shifr', sa.String(length=64), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('deadline', sa.Date(), nullable=True),
        sa.Column('workload', sa.Integer(), nullable=True),
    )
    op.create_table('workers',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('fio', sa.String(length=200), nullable=False),
        sa.Column('position', sa.String(length=100), nullable=True),
    )
    op.create_table('assignments',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=False),
        sa.Column('worker_id', sa.Integer(), sa.ForeignKey('workers.id'), nullable=False),
        sa.Column('issue_date', sa.Date(), nullable=True),
        sa.Column('planned_end', sa.Date(), nullable=True),
        sa.Column('real_end', sa.Date(), nullable=True),
        sa.Column('workload', sa.Integer(), nullable=True),
    )


def downgrade():
    op.drop_table('assignments')
    op.drop_table('workers')
    op.drop_table('projects')
