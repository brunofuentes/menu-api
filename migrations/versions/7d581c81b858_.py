"""empty message

Revision ID: 7d581c81b858
Revises: None
Create Date: 2022-08-16 20:07:57.848587

"""

# revision identifiers, used by Alembic.
revision = '7d581c81b858'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('items')
    op.drop_table('restaurants')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('restaurants',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('restaurants_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('slug', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('city', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('state', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('address', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('phone', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('imageUrl', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('websiteUrl', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('instagramUrl', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('facebookUrl', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='restaurants_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('items',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('section', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('shortDescription', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('price', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('imageUrl', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('categories', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=True),
    sa.Column('restaurant_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurants.id'], name='items_restaurant_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='items_pkey')
    )
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('phone', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('address', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('restaurant_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurants.id'], name='users_restaurant_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='users_pkey')
    )
    # ### end Alembic commands ###
