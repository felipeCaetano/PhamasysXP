import secrets
from datetime import datetime, timedelta

class SecurityUtils:
    @staticmethod
    def gerar_token_recuperacao(tamanho=32):
        """
        Gera um token de recuperação de senha seguro
        """
        return secrets.token_urlsafe(tamanho)

    @staticmethod
    def token_expirado(criado_em: datetime, validade_horas: int = 2):
        """
        Verifica se um token está expirado
        """
        expiracao = criado_em + timedelta(hours=validade_horas)
        return datetime.utcnow() > expiracao