"""Adding columns to Venue and Artist tables

Revision ID: 169b44b00f30
Revises: 18cc87c9fe76
Create Date: 2021-02-28 10:47:06.665552

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '169b44b00f30'
down_revision = '18cc87c9fe76'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('seeking_description', sa.String(length=800), nullable=True))
    op.add_column('Artist', sa.Column('seeking_venue', sa.Boolean(), nullable=True))
    op.add_column('Artist', sa.Column('shows', sa.ARRAY(sa.String(length=120)), nullable=True))
    op.add_column('Artist', sa.Column('website', sa.String(length=500), nullable=True))
    op.add_column('Venue', sa.Column('genres', sa.ARRAY(sa.String(length=120)), nullable=True))
    op.add_column('Venue', sa.Column('seeking_description', sa.String(length=800), nullable=True))
    op.add_column('Venue', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    op.add_column('Venue', sa.Column('shows', sa.ARRAY(sa.String(length=120)), nullable=True))
    op.add_column('Venue', sa.Column('website', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'website')
    op.drop_column('Venue', 'shows')
    op.drop_column('Venue', 'seeking_talent')
    op.drop_column('Venue', 'seeking_description')
    op.drop_column('Venue', 'genres')
    op.drop_column('Artist', 'website')
    op.drop_column('Artist', 'shows')
    op.drop_column('Artist', 'seeking_venue')
    op.drop_column('Artist', 'seeking_description')
    # ### end Alembic commands ###
