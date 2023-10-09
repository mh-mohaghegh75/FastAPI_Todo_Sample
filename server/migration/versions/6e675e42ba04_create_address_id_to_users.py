"""create address_id to users

Revision ID: 6e675e42ba04
Revises: bf75bab1201e
Create Date: 2023-09-15 00:42:37.115409

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '6e675e42ba04'
down_revision: Union[str, None] = 'bf75bab1201e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("address_id", sa.Integer, nullable=False))
    op.create_foreign_key('address_users_dk', source_table="users", referent_table="address",
                          local_cols=["address_id"], remote_cols=["id"], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint("address_users_fk", table_name="users")
    op.drop_column("users", "address_id")
