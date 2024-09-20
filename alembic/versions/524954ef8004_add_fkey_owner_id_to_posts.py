"""add fkey owner_id to posts

Revision ID: 524954ef8004
Revises: e83abbc28c33
Create Date: 2024-09-20 17:48:40.129500

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '524954ef8004'
down_revision: Union[str, None] = 'e83abbc28c33'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column("posts", sa.Column("owner_id", sa.Integer, nullable=False))    
    op.create_foreign_key("posts_users_fk", 
                         source_table="posts", 
                         referent_table="users", 
                         local_cols=["owner_id"], 
                         remote_cols=["id"], 
                         ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
