"""removed client_trading model

Revision ID: 09951299b303
Revises: 12a99eeb9c9e
Create Date: 2023-02-28 18:45:06.864782

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09951299b303'
down_revision = '12a99eeb9c9e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('client_trading_bonds')
    with op.batch_alter_table('admins', schema=None) as batch_op:
        batch_op.add_column(sa.Column('assigned_user', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'clients', ['assigned_user'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admins', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('assigned_user')

    op.create_table('client_trading_bonds',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('date_assigned', sa.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###