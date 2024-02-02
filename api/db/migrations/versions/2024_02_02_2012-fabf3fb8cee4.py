"""Added User to icon columns.

Revision ID: fabf3fb8cee4
Revises: e5d8cd1a0b67
Create Date: 2024-02-02 20:12:16.503940

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fabf3fb8cee4"
down_revision: Union[str, None] = "e5d8cd1a0b67"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("icon", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "icon")
    # ### end Alembic commands ###
