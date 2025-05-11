"""Initial tables

Revision ID: 10ae90edd976
Revises: 
Create Date: 2025-03-05 16:17:57.188536

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '10ae90edd976'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('api_key', sa.String(255), nullable=False, unique=True),
    )

    op.create_table(
        'tweets',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('author_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        'media',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('file_body', sa.LargeBinary, nullable=False),
        sa.Column('uploaded_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('tweet_id', sa.Integer, sa.ForeignKey('tweets.id')),
    )

    op.create_table(
        'likes',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('tweet_id', sa.Integer, sa.ForeignKey('tweets.id'), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        'follows',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('follower_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('followed_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
    )

def downgrade() -> None:
    op.drop_table('follows')
    op.drop_table('likes')
    op.drop_table('media')
    op.drop_table('tweets')
    op.drop_table('users')
