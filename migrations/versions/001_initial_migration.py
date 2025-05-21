"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-05-21 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Создаем таблицу users
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Создаем таблицу books
    op.create_table('books',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('author', sa.String(), nullable=False),
        sa.Column('publication_year', sa.Integer(), nullable=True),
        sa.Column('isbn', sa.String(), nullable=True),
        sa.Column('copies_available', sa.Integer(), nullable=False, default=1),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('isbn')
    )

    # Создаем таблицу readers
    op.create_table('readers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Создаем таблицу borrowed_books
    op.create_table('borrowed_books',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('book_id', sa.Integer(), nullable=False),
        sa.Column('reader_id', sa.Integer(), nullable=False),
        sa.Column('borrow_date', sa.DateTime(), nullable=False),
        sa.Column('return_date', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
        sa.ForeignKeyConstraint(['reader_id'], ['readers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('borrowed_books')
    op.drop_table('readers')
    op.drop_table('books')
    op.drop_table('users')
