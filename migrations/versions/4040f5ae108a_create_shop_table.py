"""create shop table

Revision ID: 4040f5ae108a
Revises: 
Create Date: 2023-05-09 02:09:24.690297

"""
from alembic import op
import sqlalchemy as sa
import litestar.contrib.sqlalchemy.types


from geoalchemy2 import Geography

# revision identifiers, used by Alembic.
revision = "4040f5ae108a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_geospatial_table(
        "shop",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("address", sa.String(), nullable=False),
        sa.Column(
            "coordinates",
            Geography(
                geometry_type="POINT",
                srid=4326,
                spatial_index=False,
                from_text="ST_GeogFromText",
                name="geography",
                nullable=False,
            ),
            nullable=False,
        ),
        sa.Column("id", litestar.contrib.sqlalchemy.types.GUID(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_shop")),
        sa.UniqueConstraint("name", name=op.f("uq_shop_name")),
    )
    op.create_geospatial_index(
        "idx_shop_coordinates",
        "shop",
        ["coordinates"],
        unique=False,
        postgresql_using="gist",
        postgresql_ops={},
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_geospatial_index(
        "idx_shop_coordinates",
        table_name="shop",
        postgresql_using="gist",
        column_name="coordinates",
    )
    op.drop_geospatial_table("shop")
    # ### end Alembic commands ###