"""update_sessions_timezone

Revision ID: 92c9d932c597
Revises: d8593bfc19a2
Create Date: 2025-03-01 17:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '92c9d932c597'
down_revision: Union[str, None] = 'd8593bfc19a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Изменяем тип столбцов с датами в таблице sessions
    op.alter_column('sessions', 'expires_at',
               existing_type=sa.DateTime(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False)
    op.alter_column('sessions', 'created_at',
               existing_type=sa.DateTime(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=True,
               existing_server_default=sa.text('now()'))
    op.alter_column('sessions', 'updated_at',
               existing_type=sa.DateTime(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=True,
               existing_server_default=sa.text('now()'))


def downgrade() -> None:
    # Возвращаем тип столбцов с датами в таблице sessions
    op.alter_column('sessions', 'updated_at',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=True,
               existing_server_default=sa.text('now()'))
    op.alter_column('sessions', 'created_at',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=True,
               existing_server_default=sa.text('now()'))
    op.alter_column('sessions', 'expires_at',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=False)
