"""timeworkSS

Revision ID: 9d01b7827405
Revises: 52be5216a2c2
Create Date: 2020-02-03 00:42:56.869343

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d01b7827405'
down_revision = '52be5216a2c2'
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