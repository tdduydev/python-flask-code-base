"""Initialize Role Table

Revision ID: 169f10c04e37
Revises: c97e8c5a7389
Create Date: 2021-12-20 17:31:44.730537

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '169f10c04e37'
down_revision = 'c97e8c5a7389'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(length=80),
               nullable=False)
    op.drop_column('user', 'is_admin')
    op.drop_column('user', 'updated_by')
    op.drop_column('user', 'is_super_admin')
    op.drop_column('user', 'created_at')
    op.drop_column('user', 'created_by')
    op.drop_column('user', 'updated_at')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('created_by', sa.TEXT(), server_default=sa.text('CURRENT_USER'), autoincrement=False, nullable=False))
    op.add_column('user', sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=False))
    op.add_column('user', sa.Column('is_super_admin', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('updated_by', sa.TEXT(), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('is_admin', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=True))
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(length=80),
               nullable=True)
    # ### end Alembic commands ###
