"""add new field in product table

Revision ID: c8b5685d8069
Revises: e1b149012a7e
Create Date: 2024-03-09 20:20:14.728965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8b5685d8069'
down_revision = 'e1b149012a7e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('unique_tag', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('common_tags', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('platform', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('post_id', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_column('post_id')
        batch_op.drop_column('platform')
        batch_op.drop_column('common_tags')
        batch_op.drop_column('unique_tag')

    # ### end Alembic commands ###