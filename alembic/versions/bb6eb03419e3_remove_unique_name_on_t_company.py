"""remove unique name on t_company

Revision ID: bb6eb03419e3
Revises: 90b8167432bf
Create Date: 2023-06-05 12:00:02.321451

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb6eb03419e3'
down_revision = '90b8167432bf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('t_company_name_key', 't_company', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('t_company_name_key', 't_company', ['name'])
    # ### end Alembic commands ###
