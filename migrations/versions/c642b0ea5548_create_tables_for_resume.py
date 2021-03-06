"""Create tables for Resume

Revision ID: c642b0ea5548
Revises: 0b1d81ace6f3
Create Date: 2021-12-04 14:23:52.589510

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c642b0ea5548'
down_revision = '0b1d81ace6f3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    
    op.create_table('resumeImageFields',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('field_name', sa.String(length=100), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('field_name')
    )
    
    op.create_table('resume',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('uploaded_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.Column('submitted_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('resumeImageStorage',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('resume_id', sa.Integer(), nullable=True),
    sa.Column('field_id', sa.Integer(), nullable=True),
    sa.Column('image_path', sa.String(length=200), nullable=True),
    sa.Column('image_public_id', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['field_id'], ['resumeImageFields.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['resume_id'], ['resume.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    
    
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    
    op.drop_table('resumeImageStorage')
    
    op.drop_table('resume')
    
    op.drop_table('resumeImageFields')
    
    # ### end Alembic commands ###
