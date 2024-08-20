"""First

Revision ID: 1eeabb624368
Revises: 42bc018040dd
Create Date: 2024-08-20 12:52:40.258164

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1eeabb624368'
down_revision: Union[str, None] = '42bc018040dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
