"""add tagnews

Revision ID: ab3bc7b913b7
Revises: 068c61bdab0b
Create Date: 2021-12-29 15:23:49.176880

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab3bc7b913b7'
down_revision = '068c61bdab0b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Tag_News',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('new_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['new_id'], ['News.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['Tags.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Tag_News')
    # ### end Alembic commands ###
