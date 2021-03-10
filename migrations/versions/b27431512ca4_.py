"""empty message

Revision ID: b27431512ca4
Revises: 31e162d0f348
Create Date: 2021-03-07 17:15:07.914488

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b27431512ca4'
down_revision = '31e162d0f348'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('states', sa.Column('total', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('states', 'total')
    # ### end Alembic commands ###
