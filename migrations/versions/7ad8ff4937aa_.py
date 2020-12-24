"""empty message

Revision ID: 7ad8ff4937aa
Revises: 26353f0d2a3d
Create Date: 2020-12-24 16:28:16.216281

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ad8ff4937aa'
down_revision = '26353f0d2a3d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('states',
    sa.Column('code', sa.String(length=2), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('code')
    )
    op.create_foreign_key('links_state_code_fkey', 'links', 'states', ['state'], ['code'])
    op.create_foreign_key('scores_state_code_fkey', 'scores', 'states', ['state'], ['code'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('scores_state_code_fkey', 'scores', type_='foreignkey')
    op.drop_constraint('links_state_code_fkey', 'links', type_='foreignkey')
    op.drop_table('states')
    # ### end Alembic commands ###
