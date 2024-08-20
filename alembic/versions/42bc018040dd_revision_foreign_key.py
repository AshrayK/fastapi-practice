"""revision foreign key

Revision ID: 42bc018040dd
Revises: f79533c6c910
Create Date: 2024-08-20 12:39:05.454463

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '42bc018040dd'
down_revision: Union[str, None] = 'f79533c6c910'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fk',source_table="posts",referent_table="users",
                          local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE",onupdate="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("post_user_fk",table_name="posts")
    op.drop_column("posts","owner_id")

    pass
