"""is_assigned added

Revision ID: 9805d2f5b875
Revises: 1de93ad5df28
Create Date: 2023-02-28 21:04:15.477607

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9805d2f5b875'
down_revision = '1de93ad5df28'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('assign_traders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('trading_assistant', sa.Integer(), nullable=True),
    sa.Column('assigned_client', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['assigned_client'], ['clients.id'], name=op.f('fk_assign_traders_assigned_client_clients')),
    sa.ForeignKeyConstraint(['trading_assistant'], ['admins.id'], name=op.f('fk_assign_traders_trading_assistant_admins')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_assign_traders'))
    )
    with op.batch_alter_table('admins', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_assigned', sa.Boolean(), nullable=False))
        batch_op.drop_column('assigned_client')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admins', schema=None) as batch_op:
        batch_op.add_column(sa.Column('assigned_client', sa.INTEGER(), nullable=True))
        batch_op.drop_column('is_assigned')

    op.drop_table('assign_traders')
    # ### end Alembic commands ###
