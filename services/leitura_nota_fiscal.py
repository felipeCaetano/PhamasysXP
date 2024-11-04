import xml.etree.ElementTree as ET


def get_fornecedor(dados, ns, root):
    '''Responsáel por extrair os dados da nota.
    ex: data, hora, numero da nota'''
    for item in root.findall('.//nfe:emit', ns):
        cnpj = item.find('.//nfe:CNPJ', ns).text
        nome = item.find('.//nfe:xNome', ns).text
        nome_fantasia = getattr(
            item.find('.//nfe:xFant', ns), 'text', 'Não Informado')
        telefone = getattr(
            item.find('.//nfe:nro', ns), 'text', 'Não Informado')

        dados.append({
            'cnpj': cnpj,
            'nome': nome,
            'nome_fantasia': nome_fantasia,
            'telefone': telefone
        })
        return dados


def ler_nota_fiscal(file_path):
    dados = []
    fornecedor = []
    itens = []

    tree = ET.parse(file_path)
    root = tree.getroot()

    ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
    items = get_items(itens, ns, root)
    fornecedor = get_fornecedor(fornecedor, ns, root)
    return fornecedor, items


def get_items(itens, ns, root):
    for item in root.findall('.//nfe:det', ns):
        codigo = item.find('.//nfe:cEAN', ns).text
        descricao = item.find('.//nfe:xProd', ns).text
        valor_unitario = f'{float(item.find('.//nfe:vUnCom', ns).text):.2f}'
        quantidade = item.find('.//nfe:qCom', ns).text.strip('.0')
        valor = item.find('.//nfe:vProd', ns).text

        itens.append({
            'codigo': codigo,
            'descricao': descricao,
            'quantidade': quantidade,
            'valor unit': valor_unitario,
            'valor': valor
        })
    return itens
