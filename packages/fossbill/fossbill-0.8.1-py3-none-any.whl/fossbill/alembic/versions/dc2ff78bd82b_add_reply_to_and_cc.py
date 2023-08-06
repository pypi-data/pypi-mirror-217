"""add reply_to and cc

Revision ID: dc2ff78bd82b
Revises: 7f2749ea8845
Create Date: 2023-06-17 12:50:25.721369

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc2ff78bd82b'
down_revision = '7f2749ea8845'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('user_pref') as batch_op:
        batch_op.add_column(sa.Column('smtp_reply_to', sa.String(length=254), nullable=True))
        batch_op.add_column(sa.Column('smtp_cc', sa.String(length=508), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('user_pref') as batch_op:
        batch_op.drop_column('smtp_reply_to')
        batch_op.drop_column('smtp_cc')
