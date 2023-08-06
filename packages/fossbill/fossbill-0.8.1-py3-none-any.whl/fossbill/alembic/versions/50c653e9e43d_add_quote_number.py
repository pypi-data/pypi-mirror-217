"""Add quote number

Revision ID: 50c653e9e43d
Revises: e88981c927d4
Create Date: 2023-02-08 15:23:41.287966

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50c653e9e43d'
down_revision = 'e88981c927d4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('bill') as batch_op:
        batch_op.alter_column('number', new_column_name='bill_number')
        batch_op.add_column(sa.Column('quote_number', sa.Integer(), nullable=True))
        batch_op.drop_constraint('bill_user_id_number_key', type_='unique')
        batch_op.drop_constraint('bill_check', type_='check')
        batch_op.drop_column('draft')
        batch_op.drop_index('ix_bill_number')
        batch_op.create_index(op.f('ix_bill_bill_number'), ['bill_number'], unique=False)
        batch_op.create_index(op.f('ix_bill_quote_number'), ['quote_number'], unique=False)
        batch_op.create_unique_constraint(None, ['user_id', 'bill_number'])
        batch_op.create_unique_constraint(None, ['user_id', 'quote_number'])

def downgrade() -> None:
    with op.batch_alter_table('bill') as batch_op:
        batch_op.alter_column('bill_number', new_column_name='number')
        batch_op.drop_constraint('bill_user_id_bill_number_key', type_='unique')
        batch_op.drop_constraint('bill_user_id_quote_number_key', type_='unique')
        batch_op.drop_index(op.f('ix_bill_quote_number'))
        batch_op.drop_index(op.f('ix_bill_bill_number'))
        batch_op.drop_column('quote_number')
        batch_op.create_index('ix_bill_number', ['number'], unique=False)
        batch_op.create_unique_constraint('bill_user_id_number_key', ['user_id', 'number'])
        batch_op.add_column(sa.Column('draft', sa.Boolean(), nullable=False, server_default='FALSE')),
        batch_op.create_check_constraint('bill_check', 'draft is TRUE or number is not NULL')
