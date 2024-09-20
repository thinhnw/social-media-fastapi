"""create posts table

Revision ID: fdc16fc3abc8
Revises: 
Create Date: 2024-09-20 16:50:07.134081

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fdc16fc3abc8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("content", sa.String, nullable=False),
        sa.Column("published", 
                  sa.Boolean, 
                  nullable=False, 
                  server_default="TRUE"),
        sa.Column("created_at", 
                  sa.TIMESTAMP(timezone=True), 
                  nullable=False, 
                  server_default=sa.func.now())
    )


def downgrade() -> None:
    op.drop_table("posts")