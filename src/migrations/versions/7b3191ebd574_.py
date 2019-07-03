"""empty message

Revision ID: 7b3191ebd574
Revises: 4aa52b9dad41
Create Date: 2019-07-02 10:31:24.444212

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b3191ebd574'
down_revision = '4aa52b9dad41'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('instance',
    sa.Column('iid', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('instance_id', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('iid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('instance')
    # ### end Alembic commands ###