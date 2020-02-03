"""active7

Revision ID: f4d83c2d82ec
Revises: 161121454328
Create Date: 2020-02-03 15:58:26.139717

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f4d83c2d82ec'
down_revision = '161121454328'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tasks', 'active',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('tasks', 'active_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('tasks', 'finish',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tasks', 'finish',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('tasks', 'active_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('tasks', 'active',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###
