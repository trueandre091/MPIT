"""add_role_to_users

Revision ID: 654396396c11
Revises: 68cd44049992
Create Date: 2025-02-19 18:15:47.837514

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '654396396c11'
down_revision: Union[str, None] = '68cd44049992'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Добавляем колонку role с значением по умолчанию "user"
    op.add_column('users', sa.Column('role', sa.String(), nullable=True))
    op.execute("UPDATE users SET role = 'user' WHERE role IS NULL")
    op.alter_column('users', 'role', nullable=False, server_default='user')


def downgrade() -> None:
    # Удаляем колонку role
    op.drop_column('users', 'role')
