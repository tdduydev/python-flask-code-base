"""update news_id

Revision ID: 34faf787cdcc
Revises: ab3bc7b913b7
Create Date: 2021-12-29 16:07:12.514038

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34faf787cdcc'
down_revision = 'ab3bc7b913b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Tag_News', sa.Column('news_id', sa.Integer(), nullable=False))
    op.drop_constraint('Tag_News_new_id_fkey', 'Tag_News', type_='foreignkey')
    op.create_foreign_key(None, 'Tag_News', 'News', ['news_id'], ['id'])
    op.drop_column('Tag_News', 'new_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Tag_News', sa.Column('new_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'Tag_News', type_='foreignkey')
    op.create_foreign_key('Tag_News_new_id_fkey', 'Tag_News', 'News', ['new_id'], ['id'])
    op.drop_column('Tag_News', 'news_id')
    # ### end Alembic commands ###
