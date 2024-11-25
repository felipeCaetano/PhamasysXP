# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

# Ajuste o import conforme sua estrutura
from models.auth import Usuario, PerfilUsuario

# URL para SQLite em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Criar engine - echo=True mostra as queries SQL no console
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False}  # Necessário apenas para SQLite
)

# Criar fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar sessão thread-safe
db_session = scoped_session(SessionLocal)

# Base declarativa para os modelos
Base = declarative_base()
Base.query = db_session.query_property()

# Função para obter a sessão do DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Função para inicializar o banco de dados
def init_db():
    # Importe todos os modelos aqui
    Base.metadata.create_all(bind=engine)

# Função para limpar o banco (útil para testes)
def clear_db():
    Base.metadata.drop_all(bind=engine)