"""Merging two heads

Revision ID: 0014bfe3ca80
Revises: 15a1538e6e95, 9119d9691444
Create Date: 2021-12-27 15:34:50.517279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0014bfe3ca80'
down_revision = ('15a1538e6e95', '9119d9691444')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
