"""timeworkingtext

Revision ID: cdcb45333b07
Revises: 8eaa4bf2ae61
Create Date: 2020-02-03 02:44:51.238381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cdcb45333b07'
down_revision = '8eaa4bf2ae61'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('time_working', sa.text(), nullable=True))
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tasks', 'time_working')
    # ### end Alembic commands ###