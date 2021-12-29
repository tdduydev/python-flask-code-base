"""Added deleted_at for News

Revision ID: 6efdb3eb73fe
Revises: fb07d9a7418f
Create Date: 2021-12-28 16:36:08.297611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6efdb3eb73fe'
down_revision = 'fb07d9a7418f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('News', sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('News', 'deleted_at')
    # ### end Alembic commands ###
