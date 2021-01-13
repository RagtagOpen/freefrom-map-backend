"""empty message

Revision ID: 86927994d09e
Revises: ea276fcdfa35
Create Date: 2021-01-12 22:44:54.225878

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86927994d09e'
down_revision = 'ea276fcdfa35'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('state_category_type', 'category_links', ['state', 'category_id', 'type'], unique=True)
    op.drop_index('state_category', table_name='category_links')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('state_category', 'category_links', ['state', 'category_id'], unique=False)
    op.drop_index('state_category_type', table_name='category_links')
    # ### end Alembic commands ###
