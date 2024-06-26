"""Add profile_pic_url

Revision ID: 947b9da0d6f3
Revises: ea07de1bb133
Create Date: 2023-06-14 13:30:26.337429

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '947b9da0d6f3'
down_revision = 'ea07de1bb133'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('t_company', sa.Column('profile_pic_url', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('t_company', 'profile_pic_url')
    # ### end Alembic commands ###
