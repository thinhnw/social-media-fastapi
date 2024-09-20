"""create users table

Revision ID: e83abbc28c33
Revises: fdc16fc3abc8
Create Date: 2024-09-20 17:42:24.793168

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e83abbc28c33'
down_revision: Union[str, None] = 'fdc16fc3abc8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("email", sa.String, nullable=False),
        sa.Column("hashed_password", sa.String, nullable=False),
        sa.Column("created_at", 
                  sa.TIMESTAMP(timezone=True), 
                  nullable=False, 
                  server_default=sa.func.now()),
        sa.UniqueConstraint("email"),
    )


def downgrade() -> None:
    op.drop_table("users")


