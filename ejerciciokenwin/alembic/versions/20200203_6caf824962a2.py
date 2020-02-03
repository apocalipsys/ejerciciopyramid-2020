"""timeworkingtext2ww

Revision ID: 6caf824962a2
Revises: 558df8513a32
Create Date: 2020-02-03 02:52:44.039108

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6caf824962a2'
down_revision = '558df8513a32'
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