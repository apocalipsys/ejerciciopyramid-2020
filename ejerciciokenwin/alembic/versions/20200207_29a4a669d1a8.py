"""localization

Revision ID: 29a4a669d1a8
Revises: 09bed1b90788
Create Date: 2020-02-07 02:45:59.377319

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29a4a669d1a8'
down_revision = '09bed1b90788'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blogposts', sa.Column('city_name', sa.Text(), nullable=True))
    op.add_column('blogposts', sa.Column('country_name', sa.Text(), nullable=True))
    op.add_column('blogposts', sa.Column('ip', sa.Text(), nullable=True))
    op.add_column('blogposts', sa.Column('province_name', sa.Text(), nullable=True))
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('blogposts', 'province_name')
    op.drop_column('blogposts', 'ip')
    op.drop_column('blogposts', 'country_name')
    op.drop_column('blogposts', 'city_name')
    # ### end Alembic commands ###
