"""Table

Revision ID: 8a165c974df5
Revises: 10ae90edd976
Create Date: 2025-03-08 23:01:33.193744

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a165c974df5'
down_revision: Union[str, None] = '10ae90edd976'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table('media')

    op.create_table(
        'media',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('file_body', sa.LargeBinary, nullable=False),
        sa.Column('uploaded_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('tweet_id', sa.Integer, sa.ForeignKey('tweets.id'))
    )


def downgrade() -> None:
    op.drop_table('media')

