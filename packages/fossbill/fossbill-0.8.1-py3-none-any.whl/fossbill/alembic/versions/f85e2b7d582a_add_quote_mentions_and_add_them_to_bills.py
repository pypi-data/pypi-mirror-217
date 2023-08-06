"""Add quote mentions and add them to bills

Revision ID: f85e2b7d582a
Revises: 50c653e9e43d
Create Date: 2023-02-09 11:16:38.322313

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f85e2b7d582a'
down_revision = '50c653e9e43d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('user_pref') as batch_op:
        batch_op.alter_column('mentions', new_column_name='quote_mentions')
        batch_op.add_column(sa.Column('bill_mentions', sa.String(length=500), nullable=True))
    with op.batch_alter_table('bill') as batch_op:
        batch_op.add_column(sa.Column('quote_mentions', sa.String(length=500), nullable=True))
        batch_op.add_column(sa.Column('bill_mentions', sa.String(length=500), nullable=True))

def downgrade() -> None:
    with op.batch_alter_table('user_pref') as batch_op:
        batch_op.alter_column('quote_mentions', new_column_name='mentions')
        batch_op.drop_column('bill_mentions')
    with op.batch_alter_table('bill') as batch_op:
        batch_op.drop_column('quote_mentions')
        batch_op.drop_column('bill_mentions')
