"""initial

Revision ID: 122e758c6427
Revises: 
Create Date: 2017-04-26 20:49:52.480282

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '122e758c6427'
down_revision = None
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
    op.create_table('quotes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('author', sa.Text(), nullable=True),
    sa.Column('source', sa.Text(), nullable=True),
    sa.Column('link', sa.Text(), nullable=True),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('default', sa.Boolean(), nullable=True),
    sa.Column('permissions', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_roles_default'), 'roles', ['default'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_roles_default'), table_name='roles')
    op.drop_table('roles')
    op.drop_table('quotes')
    op.drop_index(op.f('ix_messages_nick'), table_name='messages')
    op.drop_index(op.f('ix_messages_channel'), table_name='messages')
    op.drop_table('messages')
    # ### end Alembic commands ###