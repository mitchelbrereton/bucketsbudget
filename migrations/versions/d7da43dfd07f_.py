"""empty message

Revision ID: d7da43dfd07f
Revises: 64264654a34f
Create Date: 2020-05-19 21:24:39.234668

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7da43dfd07f'
down_revision = '64264654a34f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('budget', sa.Column('est_min', sa.Float(), nullable=True))
    op.add_column('budget', sa.Column('next_due', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_budget_next_due'), 'budget', ['next_due'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_budget_next_due'), table_name='budget')
    op.drop_column('budget', 'next_due')
    op.drop_column('budget', 'est_min')
    # ### end Alembic commands ###