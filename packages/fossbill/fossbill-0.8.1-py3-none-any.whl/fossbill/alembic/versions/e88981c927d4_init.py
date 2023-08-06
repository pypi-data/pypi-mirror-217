"""Init

Revision ID: e88981c927d4
Revises: 
Create Date: 2023-02-08 14:22:03.272820

"""
from alembic import op
import sqlalchemy as sa
from fossbill.database import get_db
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = 'e88981c927d4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    engine, metadata = get_db()
    insp = inspect(engine)
    tables = insp.get_table_names()

    if 'user' not in tables:
        op.create_table('user',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('password', sa.String(length=120), nullable=False),
            sa.Column('username', sa.String(length=50), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('username')
        )

    if 'client' not in tables:
        op.create_table('client',
            sa.Column('address', sa.String(length=500), nullable=True),
            sa.Column('currency', sa.String(length=10), nullable=True),
            sa.Column('email', sa.String(length=70), nullable=True),
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('label', sa.String(length=40), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_client_user_id'), 'client', ['user_id'], unique=False)

    if 'product' not in tables:
        op.create_table('product',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('label', sa.String(length=120), nullable=False),
            sa.Column('price', sa.Integer(), nullable=False),
            sa.Column('tax_rate', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_product_user_id'), 'product', ['user_id'], unique=False)

    if 'user_pref' not in tables:
        op.create_table('user_pref',
            sa.Column('currency', sa.String(length=10), nullable=True),
            sa.Column('email', sa.String(length=70), nullable=True),
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('mentions', sa.String(length=500), nullable=True),
            sa.Column('smtp_host', sa.String(length=30), nullable=True),
            sa.Column('smtp_password', sa.String(length=30), nullable=True),
            sa.Column('smtp_port', sa.Integer(), nullable=True),
            sa.Column('smtp_security', sa.String(length=10), nullable=True),
            sa.Column('smtp_username', sa.String(length=30), nullable=True),
            sa.Column('source', sa.String(length=500), nullable=True),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_user_pref_user_id'), 'user_pref', ['user_id'], unique=False)

    if 'bill' not in tables:
        op.create_table('bill',
            sa.Column('amount', sa.Integer(), nullable=False),
            sa.Column('client_id', sa.Integer(), nullable=True),
            sa.Column('comment', sa.String(length=500), nullable=True),
            sa.Column('currency', sa.String(length=10), nullable=True),
            sa.Column('date', sa.Date(), nullable=False),
            sa.Column('draft', sa.Boolean(), nullable=False),
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('number', sa.Integer(), nullable=True),
            sa.Column('recipient', sa.String(length=500), nullable=False),
            sa.Column('source', sa.String(length=500), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.CheckConstraint('draft is TRUE or number is not NULL'),
            sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
            sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('user_id', 'number')
        )
        op.create_index(op.f('ix_bill_client_id'), 'bill', ['client_id'], unique=False)
        op.create_index(op.f('ix_bill_number'), 'bill', ['number'], unique=False)
        op.create_index(op.f('ix_bill_user_id'), 'bill', ['user_id'], unique=False)

    if 'bill_row' not in tables:
        op.create_table('bill_row',
            sa.Column('bill_id', sa.Integer(), nullable=False),
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('label', sa.String(length=120), nullable=False),
            sa.Column('price', sa.Integer(), nullable=False),
            sa.Column('quantity', sa.Integer(), nullable=False),
            sa.Column('tax_rate', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['bill_id'], ['bill.id'], ),
            sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_bill_row_bill_id'), 'bill_row', ['bill_id'], unique=False)
        op.create_index(op.f('ix_bill_row_user_id'), 'bill_row', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_bill_row_user_id'), table_name='bill_row')
    op.drop_index(op.f('ix_bill_row_bill_id'), table_name='bill_row')
    op.drop_table('bill_row')
    op.drop_index(op.f('ix_bill_user_id'), table_name='bill')
    op.drop_index(op.f('ix_bill_number'), table_name='bill')
    op.drop_index(op.f('ix_bill_client_id'), table_name='bill')
    op.drop_table('bill')
    op.drop_index(op.f('ix_user_pref_user_id'), table_name='user_pref')
    op.drop_table('user_pref')
    op.drop_index(op.f('ix_product_user_id'), table_name='product')
    op.drop_table('product')
    op.drop_index(op.f('ix_client_user_id'), table_name='client')
    op.drop_table('client')
    op.drop_table('user')
