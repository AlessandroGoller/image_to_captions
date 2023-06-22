"""remove unique to unique_hash_code

Revision ID: a044c1383e26
Revises: 318576544037
Create Date: 2023-06-21 16:20:39.428945

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a044c1383e26'
down_revision = '318576544037'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('t_telegram_unique_hash_code_key', 't_telegram', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('t_telegram_unique_hash_code_key', 't_telegram', ['unique_hash_code'])
    # ### end Alembic commands ###