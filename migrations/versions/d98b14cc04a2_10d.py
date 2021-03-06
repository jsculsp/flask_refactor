"""10d

Revision ID: d98b14cc04a2
Revises: 4f72303a7f20
Create Date: 2016-10-04 16:29:44.407713

"""

# revision identifiers, used by Alembic.
revision = 'd98b14cc04a2'
down_revision = '4f72303a7f20'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('avatar_hash', sa.String(length=32), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar_hash')
    ### end Alembic commands ###
