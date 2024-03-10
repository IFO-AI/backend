"""update db field

Revision ID: 0ce917284da1
Revises: dd9092234ce5
Create Date: 2024-03-10 08:43:42.264534

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ce917284da1'
down_revision = 'dd9092234ce5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.alter_column('reply_message_id',
               existing_type=sa.TEXT(),
               type_=sa.Integer(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.alter_column('reply_message_id',
               existing_type=sa.Integer(),
               type_=sa.TEXT(),
               existing_nullable=True)

    # ### end Alembic commands ###
