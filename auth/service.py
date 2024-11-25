import bcrypt
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.auth import Usuario, PerfilUsuario
from .schemas import UsuarioSchema

class AuthService:
    """"""
    # _hash_senha, verificar_senha, criar_usuario, etc.
    # ... (código do serviço de autenticação)