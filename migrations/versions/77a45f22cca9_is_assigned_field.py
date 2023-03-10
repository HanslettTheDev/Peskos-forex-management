"""is_assigned field

Revision ID: 77a45f22cca9
Revises: ff46b1d6a4ef
Create Date: 2023-03-06 08:14:06.321374

"""
from alembic import op
from sqlalchemy.sql import false
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77a45f22cca9'
down_revision = 'ff46b1d6a4ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admins', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_assigned', sa.Boolean(), nullable=False, server_default=false()))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admins', schema=None) as batch_op:
        batch_op.drop_column('is_assigned')

    # ### end Alembic commands ###
