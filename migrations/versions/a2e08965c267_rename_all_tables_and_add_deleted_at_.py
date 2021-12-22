"""Rename all tables and add deleted_at for Role, User

Revision ID: a2e08965c267
Revises: 874f958187d5
Create Date: 2021-12-22 16:46:42.517904

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2e08965c267'
down_revision = '874f958187d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_with_role',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['Role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'role_id')
    )
    op.drop_table('User_Role')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('User_Role',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('role_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['Role.id'], name='user_with_role_role_id_fkey1'),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], name='user_with_role_user_id_fkey1'),
    sa.PrimaryKeyConstraint('user_id', 'role_id', name='user_with_role_pkey1')
    )
    op.drop_table('user_with_role')
    # ### end Alembic commands ###
