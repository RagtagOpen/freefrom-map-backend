"""empty message

Revision ID: bb239b87fe29
Revises: ea276fcdfa35
Create Date: 2021-01-13 23:02:46.608601

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb239b87fe29'
down_revision = 'ea276fcdfa35'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('links', sa.Column('created_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('links', 'created_at')
    # ### end Alembic commands ###