"""create phone number for user call

Revision ID: 17da57d72a64
Revises: 
Create Date: 2023-09-14 23:46:51.463020

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '17da57d72a64'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("country_code", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "phone_number")
