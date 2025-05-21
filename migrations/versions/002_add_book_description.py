"""Add book description

Revision ID: 002
Revises: 001
Create Date: 2024-05-21 12:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Добавляем поле description к таблице books
    op.add_column('books',
        sa.Column('description', sa.String(), nullable=True)
    )
    
    # Устанавливаем значение по умолчанию для существующих записей
    op.execute("UPDATE books SET description = 'No description available' WHERE description IS NULL")

def downgrade() -> None:
    op.drop_column('books', 'description')
