"""11f

Revision ID: ae9b600acb5f
Revises: 110d62da87a0
Create Date: 2016-10-05 12:45:25.263430

"""

# revision identifiers, used by Alembic.
revision = 'ae9b600acb5f'
down_revision = '110d62da87a0'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('body_html', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'body_html')
    ### end Alembic commands ###
