from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings import get_settings
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

st = get_settings()

def create_db():
    # Подключаемся к базе postgres вместо целевой базы данных
    conn = psycopg2.connect(
        host=st.POSTGRES_HOST,
        port=st.POSTGRES_PORT,
        database="postgres",  # Используем стандартную базу postgres для подключения
        user=st.POSTGRES_USER,
        password=st.POSTGRES_PASSWORD
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cur = conn.cursor()
    try:
        # Проверяем, существует ли база данных
        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{st.POSTGRES_DB}'")
        exists = cur.fetchone()
        
        if not exists:
            cur.execute(f'CREATE DATABASE {st.POSTGRES_DB}')
            print(f'База данных {st.POSTGRES_DB} успешно создана')
        else:
            print(f'База данных {st.POSTGRES_DB} уже существует')
            
    except Exception as e:
        print(f'Ошибка при создании базы данных: {e}')
    finally:
        cur.close()
        conn.close()

SQLALCHEMY_DATABASE_URL = f"postgresql://{st.POSTGRES_USER}:{st.POSTGRES_PASSWORD}@{st.POSTGRES_HOST}:{st.POSTGRES_PORT}/{st.POSTGRES_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    if not st.DB_CREATED:
        create_db()
        st.DB_CREATED = True
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
