"""added country, city, website, gmaps_link to shops

Revision ID: ee75c4426a69
Revises: e001efbbf4da
Create Date: 2023-06-21 23:57:41.301206

"""
from alembic import op
import sqlalchemy as sa
import litestar.contrib.sqlalchemy.types



# revision identifiers, used by Alembic.
revision = 'ee75c4426a69'
down_revision = 'e001efbbf4da'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shop', sa.Column('country', sa.String(), nullable=False))
    op.add_column('shop', sa.Column('city', sa.String(), nullable=False))
    op.add_column('shop', sa.Column('website', sa.String(), nullable=True))
    op.add_column('shop', sa.Column('gmaps_link', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('shop', 'gmaps_link')
    op.drop_column('shop', 'website')
    op.drop_column('shop', 'city')
    op.drop_column('shop', 'country')
    # ### end Alembic commands ###
