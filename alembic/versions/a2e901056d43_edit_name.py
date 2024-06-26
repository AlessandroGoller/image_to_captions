"""edit name

Revision ID: a2e901056d43
Revises: 1f1bea04152a
Create Date: 2023-06-07 15:40:18.694691

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2e901056d43'
down_revision = '1f1bea04152a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('t_user', sa.Column('data_last_paid', sa.DateTime(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('t_user', 'data_last_paid')
    # ### end Alembic commands ###
