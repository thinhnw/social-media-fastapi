"""create votes table

Revision ID: 1d10640d644c
Revises: 524954ef8004
Create Date: 2024-09-20 17:54:36.135753

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d10640d644c'
down_revision: Union[str, None] = '524954ef8004'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "votes",
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("post_id", sa.Integer, nullable=False),
        sa.PrimaryKeyConstraint("user_id", "post_id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"], ondelete="CASCADE"),
    )


def downgrade() -> None:
    op.drop_table("votes")
