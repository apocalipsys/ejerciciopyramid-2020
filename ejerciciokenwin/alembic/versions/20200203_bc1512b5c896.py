"""active

Revision ID: bc1512b5c896
Revises: 7510cd1075a2
Create Date: 2020-02-03 15:31:18.263690

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc1512b5c896'
down_revision = '7510cd1075a2'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('active', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tasks', 'active')
    # ### end Alembic commands ###
