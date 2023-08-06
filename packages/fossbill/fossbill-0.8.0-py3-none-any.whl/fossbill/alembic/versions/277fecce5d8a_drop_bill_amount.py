"""empty message

Revision ID: 277fecce5d8a
Revises: 0321467f0761
Create Date: 2023-04-27 11:02:36.866204

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '277fecce5d8a'
down_revision = '0321467f0761'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('bill') as batch_op:
        batch_op.drop_column('amount')


def downgrade() -> None:
    with op.batch_alter_table('bill') as batch_op:
        batch_op.add_column(sa.Column('bill_mentions', sa.Integer(), nullable=True))
