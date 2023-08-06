"""empty message

Revision ID: 0321467f0761
Revises: f85e2b7d582a
Create Date: 2023-04-24 08:54:58.368012

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0321467f0761'
down_revision = 'f85e2b7d582a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('user_pref') as batch_op:
        batch_op.add_column(sa.Column('locale', sa.String(length=10), nullable=False, server_default='en_US'))


def downgrade() -> None:
    with op.batch_alter_table('user_pref') as batch_op:
        batch_op.drop_column('locale')
