import pytest
from services.leitura_nota_fiscal import ler_nota_fiscal


def test_ler_nota_fiscal():
    # Caminho para um arquivo XML de teste (substitua pelo caminho correto)
    caminho_arquivo = 'diversos/26241061412110117427650010000581831087046354-nfe.xml'

    # Chama a função que ainda não foi implementada
    itens = ler_nota_fiscal(caminho_arquivo)

    # Verifique se a lista de itens não está vazia
    assert len(itens) > 0

    # Verifique se os itens têm as chaves esperadas
    for item in itens:
        assert 'codigo' in item
        assert 'descricao' in item
        assert 'quantidade' in item
        assert 'valor' in item
