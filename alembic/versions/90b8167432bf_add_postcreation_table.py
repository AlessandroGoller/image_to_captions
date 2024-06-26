"""add postcreation table

Revision ID: 90b8167432bf
Revises: 31ac00618098
Create Date: 2023-05-29 16:34:55.138328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90b8167432bf'
down_revision = '31ac00618098'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('t_post_creation',
    sa.Column('id_t_post_creation', sa.Integer(), nullable=False),
    sa.Column('id_t_user', sa.Integer(), nullable=False),
    sa.Column('image_uploaded', sa.LargeBinary(), nullable=True),
    sa.Column('Description', sa.String(), nullable=True),
    sa.Column('prompt', sa.Text(), nullable=True),
    sa.Column('post_created', sa.Text(), nullable=True),
    sa.Column('refinement', sa.JSON(), nullable=True),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['id_t_user'], ['t_user.id_t_user'], ),
    sa.PrimaryKeyConstraint('id_t_post_creation')
    )
    op.add_column('t_company', sa.Column('language', sa.String(), nullable=True))
    op.create_foreign_key(None, 't_company', 't_user', ['id_user'], ['id_t_user'])
    op.drop_constraint('t_instagram_un', 't_instagram', type_='unique')
    op.add_column('t_user', sa.Column('language', sa.String(), nullable=True))
    op.add_column('t_user', sa.Column('email_confirmed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('t_user', 'email_confirmed')
    op.drop_column('t_user', 'language')
    op.create_unique_constraint('t_instagram_un', 't_instagram', ['posturl', 'id_company', 'id_user', 'post'])
    op.drop_constraint(None, 't_company', type_='foreignkey')
    op.drop_column('t_company', 'language')
    op.drop_table('t_post_creation')
    # ### end Alembic commands ###
