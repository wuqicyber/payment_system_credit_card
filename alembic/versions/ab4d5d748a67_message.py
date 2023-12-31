"""message

Revision ID: ab4d5d748a67
Revises: 6889f8688894
Create Date: 2023-06-30 17:37:11.800462

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab4d5d748a67'
down_revision = '6889f8688894'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('remained_unpaid_amount', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transactions', 'remained_unpaid_amount')
    # ### end Alembic commands ###
