"""Update User inform

Revision ID: c97e8c5a7389
Revises: cc1d05b02573
Create Date: 2021-12-15 09:00:20.102647

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c97e8c5a7389'
down_revision = 'cc1d05b02573'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('lastName', sa.String(length=80), nullable=True))
    op.add_column('user', sa.Column('firstName', sa.String(length=80), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'firstName')
    op.drop_column('user', 'lastName')
    # ### end Alembic commands ###