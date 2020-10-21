"""empty message

Revision ID: 98c58c9a9ed2
Revises: 
Create Date: 2020-10-20 13:32:35.647037

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98c58c9a9ed2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('powerplants',
    sa.Column('facility_code', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('state_abbreviation', sa.String(length=2), nullable=True),
    sa.Column('annual_net_generation', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('facility_code')
    )
    op.create_index(op.f('ix_powerplants_annual_net_generation'), 'powerplants', ['annual_net_generation'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_powerplants_annual_net_generation'), table_name='powerplants')
    op.drop_table('powerplants')
    # ### end Alembic commands ###