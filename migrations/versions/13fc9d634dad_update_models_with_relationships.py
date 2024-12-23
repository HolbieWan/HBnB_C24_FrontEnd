"""Update models with relationships

Revision ID: 13fc9d634dad
Revises: 
Create Date: 2024-11-11 15:41:44.304201

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '13fc9d634dad'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'place_amenity',
        sa.Column('place_id', sa.String(length=36), nullable=False),
        sa.Column('amenity_id', sa.String(length=36), nullable=False),
        sa.ForeignKeyConstraint(['amenity_id'], ['amenities.id'], name='fk_place_amenity_amenity_id'),
        sa.ForeignKeyConstraint(['place_id'], ['places.id'], name='fk_place_amenity_place_id'),
        sa.PrimaryKeyConstraint('place_id', 'amenity_id')
    )

    with op.batch_alter_table('places', schema=None) as batch_op:
        batch_op.drop_column('amenities')

    with op.batch_alter_table('reviews', schema=None) as batch_op:
        batch_op.create_foreign_key('fk_reviews_place_id', 'places', ['place_id'], ['id'])
        batch_op.create_foreign_key('fk_reviews_user_id', 'users', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # Skip dropping foreign keys for reviews since they don't exist
    with op.batch_alter_table('places', schema=None) as batch_op:
        batch_op.add_column(sa.Column('amenities', sqlite.JSON(), nullable=True))

    # Drop the place_amenity table
    op.drop_table('place_amenity')