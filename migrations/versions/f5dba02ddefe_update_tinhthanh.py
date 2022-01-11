"""update tinhthanh

Revision ID: f5dba02ddefe
Revises: 51a8c1e022c0
Create Date: 2022-01-10 21:03:52.874907

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5dba02ddefe'
down_revision = '51a8c1e022c0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tinhthanh', sa.Column('deleted', sa.Boolean(), nullable=True))
    op.drop_column('tinhthanh', 'delete')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tinhthanh', sa.Column('delete', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('tinhthanh', 'deleted')
    # ### end Alembic commands ###
