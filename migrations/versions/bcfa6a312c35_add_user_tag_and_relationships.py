"""Add user, tag and relationships

Revision ID: bcfa6a312c35
Revises: cebac4d1b499
Create Date: 2025-11-20 14:33:41.332448
"""
from alembic import op
import sqlalchemy as sa

revision = 'bcfa6a312c35'
down_revision = 'cebac4d1b499'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )

    op.create_table(
        'post_tags',
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['post_id'], ['posts.id']),
        sa.ForeignKeyConstraint(['tag_id'], ['tags.id']),
        sa.PrimaryKeyConstraint('post_id', 'tag_id')
    )

    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author_id', sa.Integer(), nullable=True))

        batch_op.create_foreign_key(
            'fk_posts_author_id_users',
            'users',
            ['author_id'],
            ['id']
        )

        batch_op.drop_column('is_active')
        batch_op.drop_column('author')


def downgrade():
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author', sa.VARCHAR(length=20), nullable=False))
        batch_op.add_column(sa.Column('is_active', sa.BOOLEAN(), nullable=False))

        batch_op.drop_constraint('fk_posts_author_id_users', type_='foreignkey')

        batch_op.drop_column('author_id')


    op.drop_table('post_tags')
    op.drop_table('users')
    op.drop_table('tags')
