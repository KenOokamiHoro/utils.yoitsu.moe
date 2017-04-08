"""add Quote

Revision ID: 9f3c7bc86e22
Revises: 944fad3b2438
Create Date: 2017-04-07 20:40:23.587214

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f3c7bc86e22'
down_revision = '944fad3b2438'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('quotes', sa.Column('comment', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('quotes', 'comment')
    # ### end Alembic commands ###