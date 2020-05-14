"""empty message

Revision ID: 64264654a34f
Revises: 
Create Date: 2020-05-14 21:28:03.099398

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64264654a34f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('budget',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('group', sa.String(length=140), nullable=True),
    sa.Column('expense', sa.String(length=140), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('last_paid', sa.DateTime(), nullable=True),
    sa.Column('expense_cycle', sa.String(), nullable=True),
    sa.Column('in_flows', sa.Float(), nullable=True),
    sa.Column('out_flows', sa.Float(), nullable=True),
    sa.Column('available', sa.Float(), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['username'], ['user.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_budget_last_paid'), 'budget', ['last_paid'], unique=False)
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('expense', sa.String(length=140), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('note', sa.String(length=240), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('budget_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['budget_id'], ['budget.id'], ),
    sa.ForeignKeyConstraint(['username'], ['user.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transactions_date'), 'transactions', ['date'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_transactions_date'), table_name='transactions')
    op.drop_table('transactions')
    op.drop_index(op.f('ix_budget_last_paid'), table_name='budget')
    op.drop_table('budget')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###