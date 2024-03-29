"""remove is_assigned field

Revision ID: ff46b1d6a4ef
Revises: 9805d2f5b875
Create Date: 2023-03-05 12:08:16.507921

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff46b1d6a4ef'
down_revision = '9805d2f5b875'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_admins')
    with op.batch_alter_table('admins', schema=None) as batch_op:
        batch_op.drop_column('is_assigned')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admins', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_assigned', sa.BOOLEAN(), nullable=False))

    op.create_table('_alembic_tmp_admins',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('is_assigned', sa.BOOLEAN(), nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=100), nullable=False),
    sa.Column('last_name', sa.VARCHAR(length=100), nullable=False),
    sa.Column('email', sa.VARCHAR(length=100), nullable=False),
    sa.Column('password', sa.VARCHAR(length=150), nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), nullable=False),
    sa.PrimaryKeyConstraint('id', name='pk_admins'),
    sa.UniqueConstraint('email', name='uq_admins_email')
    )
    # ### end Alembic commands ###
