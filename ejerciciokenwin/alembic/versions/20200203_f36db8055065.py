"""active2

Revision ID: f36db8055065
Revises: bc1512b5c896
Create Date: 2020-02-03 15:32:31.205834

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f36db8055065'
down_revision = 'bc1512b5c896'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('active', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tasks', 'active')
    # ### end Alembic commands ###
