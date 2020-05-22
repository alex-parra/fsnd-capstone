"""empty message

Revision ID: 3973c38e5180
Revises: 
Create Date: 2020-05-22 10:44:53.269741

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3973c38e5180'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('movies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('release_date', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('movies')
    # ### end Alembic commands ###
