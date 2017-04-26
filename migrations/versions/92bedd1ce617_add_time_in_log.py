"""add time in log

Revision ID: 92bedd1ce617
Revises: bf566ebff1ce
Create Date: 2017-04-25 23:05:46.208527

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92bedd1ce617'
down_revision = 'bf566ebff1ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('channel', sa.String(length=64), nullable=True),
    sa.Column('nick', sa.String(length=64), nullable=True),
    sa.Column('messages', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_messages_channel'), 'messages', ['channel'], unique=False)
    op.create_index(op.f('ix_messages_nick'), 'messages', ['nick'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_messages_nick'), table_name='messages')
    op.drop_index(op.f('ix_messages_channel'), table_name='messages')
    op.drop_table('messages')
    # ### end Alembic commands ###
