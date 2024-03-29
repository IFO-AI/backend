"""added p product table

Revision ID: 86c20a1ad5fa
Revises: 2535770f91ee
Create Date: 2024-03-08 18:40:59.897121

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86c20a1ad5fa'
down_revision = '2535770f91ee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_name', sa.String(length=100), nullable=False),
    sa.Column('company_email', sa.String(length=100), nullable=False),
    sa.Column('product_title', sa.String(length=100), nullable=False),
    sa.Column('product_logo', sa.Text(), nullable=False),
    sa.Column('product_url', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('twitter_user_name', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product')
    # ### end Alembic commands ###
