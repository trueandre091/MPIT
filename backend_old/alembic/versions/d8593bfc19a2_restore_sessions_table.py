"""restore_sessions_table

Revision ID: d8593bfc19a2
Revises: b38b301cef3c
Create Date: 2025-03-01 16:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd8593bfc19a2'
down_revision: Union[str, None] = 'b38b301cef3c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Создаем таблицу сессий
    op.create_table(
        'sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('refresh_token', sa.String(), nullable=False),
        sa.Column('access_token', sa.String(), nullable=True),
        sa.Column('user_agent', sa.String(), nullable=True),
        sa.Column('ip_address', sa.String(), nullable=True),
        sa.Column('device_info', sa.JSON(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('expires_at', sa.DateTime(timezone=False), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=False), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=False), server_default=sa.text('now()')),
        
        # Первичный ключ
        sa.PrimaryKeyConstraint('id'),
        
        # Внешний ключ на таблицу пользователей
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        
        # Индексы
        sa.Index('ix_sessions_id', 'id'),
        sa.Index('ix_sessions_refresh_token', 'refresh_token', unique=True),
        sa.Index('ix_sessions_user_id', 'user_id'),
        sa.Index('ix_sessions_is_active', 'is_active'),
    )

    # Добавляем триггер для автоматического обновления updated_at
    op.execute("""
        CREATE OR REPLACE FUNCTION update_sessions_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
    """)

    op.execute("""
        CREATE TRIGGER update_sessions_updated_at
            BEFORE UPDATE
            ON sessions
            FOR EACH ROW
        EXECUTE FUNCTION update_sessions_updated_at();
    """)


def downgrade() -> None:
    # Удаляем триггер и функцию
    op.execute("DROP TRIGGER IF EXISTS update_sessions_updated_at ON sessions")
    op.execute("DROP FUNCTION IF EXISTS update_sessions_updated_at()")
    
    # Удаляем таблицу
    op.drop_table('sessions')
