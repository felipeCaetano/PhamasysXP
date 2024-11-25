import re
from typing import Optional
from pydantic import BaseModel, EmailStr, validator
from models.auth import TipoUsuario

class UsuarioSchema(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    tipo: TipoUsuario
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    crf: Optional[str] = None

    @validator('senha')
    def validar_senha(cls, senha):
        # Mesma lógica de validação de senha do exemplo anterior
        # ... (código de validação de senha)
        return senha
