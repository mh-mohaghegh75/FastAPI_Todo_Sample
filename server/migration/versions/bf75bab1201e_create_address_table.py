"""create address table

Revision ID: bf75bab1201e
Revises: 17da57d72a64
Create Date: 2023-09-14 23:56:30.273593

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'bf75bab1201e'
down_revision: Union[str, None] = '17da57d72a64'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("address",
                    sa.Column("id", sa.Integer, nullable=False, primary_key=True),
                    sa.Column("address1", sa.String(), nullable=False),
                    sa.Column("address2", sa.String(), nullable=False),
                    sa.Column("city", sa.String(), nullable=False),
                    sa.Column("country", sa.String(), nullable=False)
                    )


def downgrade() -> None:
    op.drop_table("address")
