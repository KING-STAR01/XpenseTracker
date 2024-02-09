"""initial migration

Revision ID: adb43f05b61c
Revises: ccc0a806606b
Create Date: 2024-01-09 22:41:07.192123

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'adb43f05b61c'
down_revision: Union[str, None] = 'ccc0a806606b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
