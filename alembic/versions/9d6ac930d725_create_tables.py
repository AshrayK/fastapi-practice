"""create tables

Revision ID: 9d6ac930d725
Revises: 
Create Date: 2024-08-20 10:53:34.209140

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = '9d6ac930d725'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                    sa.Column('title',sa.String(),nullable=False),
                    sa.Column('content',sa.String(),nullable=False),
                    sa.Column('published',sa.Boolean(),nullable=False, server_default="TRUE"),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False, server_default = sa.text("NOW()")))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
