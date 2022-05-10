"""empty message

Revision ID: ec47676b2382
Revises: 880a9131046f
Create Date: 2022-05-09 21:41:02.839397

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec47676b2382'
down_revision = '880a9131046f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pokedex',
    sa.Column('pd_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('hp', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('pd_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pokedex')
    # ### end Alembic commands ###
