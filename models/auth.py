from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, \
    ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class TipoUsuario(enum.Enum):
    ADMIN = "admin"
    FARMACEUTICO = "farmaceutico"
    ATENDENTE = "atendente"
    ESTOQUISTA = "estoquista"


class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    tipo = Column(Enum(TipoUsuario), nullable=False)
    ativo = Column(Boolean, default=True)

    # Campos de auditoria
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)
    ultimo_login = Column(DateTime)

    # Relacionamento com o perfil
    perfil = relationship("PerfilUsuario", back_populates="usuario",
                          uselist=False)


class PerfilUsuario(Base):
    __tablename__ = 'perfis_usuario'

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), unique=True)
    cpf = Column(String(11), unique=True)
    telefone = Column(String(20))
    endereco = Column(String(200))
    crf = Column(String(20), unique=True,
                 nullable=True)  # Registro do Farmacêutico

    # Campos de auditoria
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    # Relacionamento com usuário
    usuario = relationship("Usuario", back_populates="perfil")