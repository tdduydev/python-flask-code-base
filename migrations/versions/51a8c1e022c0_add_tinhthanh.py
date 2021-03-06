"""add tinhthanh

Revision ID: 51a8c1e022c0
Revises: 1ef8b429eee9
Create Date: 2022-01-10 21:00:26.576901

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '51a8c1e022c0'
down_revision = '1ef8b429eee9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tinhthanh',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('ma', sa.String(length=300), nullable=False),
    sa.Column('ten', sa.String(length=300), nullable=False),
    sa.Column('ten_tieng_anh', sa.String(length=300), nullable=False),
    sa.Column('loai', sa.String(length=300), nullable=False),
    sa.Column('quocgia_id', postgresql.UUID(), nullable=False),
    sa.Column('active', sa.String(), nullable=False),
    sa.Column('created_at', sa.String(length=300), nullable=False),
    sa.Column('created_by', sa.String(length=300), nullable=False),
    sa.Column('updated_at', sa.String(length=300), nullable=False),
    sa.Column('updated_by', sa.String(length=300), nullable=False),
    sa.Column('delete', sa.Boolean(), nullable=True),
    sa.Column('deleted_at', sa.String(length=300), nullable=False),
    sa.Column('deleted_by', sa.String(length=300), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tinhthanh')
    # ### end Alembic commands ###
