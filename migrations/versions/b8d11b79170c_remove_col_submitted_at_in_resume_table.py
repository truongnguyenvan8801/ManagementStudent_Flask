"""remove col submitted_at in resume table

Revision ID: b8d11b79170c
Revises: a817979962d0
Create Date: 2021-12-06 19:19:25.486597

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b8d11b79170c'
down_revision = 'a817979962d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('resume', 'submitted_at')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('resume', sa.Column('submitted_at', mysql.DATETIME(), nullable=False))
    # ### end Alembic commands ###