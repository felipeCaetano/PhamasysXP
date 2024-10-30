import xml.etree.ElementTree as ET


def get_dados_nota(dados, ns, root):
    '''Responsáel por extrair os dados da nota.
    ex: data, hora, numero da nota'''
    for item in root.findall('.//nfe:det', ns):
        codigo = item.find('.//nfe:cProd', ns).text
        descricao = item.find('.//nfe:xProd', ns).text
        quantidade = item.find('.//nfe:qCom', ns).text
        valor = item.find('.//nfe:vProd', ns).text

        dados.append({
            'codigo': codigo,
            'descricao': descricao,
            'quantidade': quantidade,
            'valor': valor
        })
        return dados


def ler_nota_fiscal(file_path):
    dados = []
    fornecedor = []
    itens = []

    tree = ET.parse(file_path)
    root = tree.getroot()

    ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
    dados_nota = get_dados_nota(dados, ns, root)
    items = get_items(itens, ns, root)
    return items


def get_items(itens, ns, root):
    for item in root.findall('.//nfe:det', ns):
        codigo = item.find('.//nfe:cProd', ns).text
        descricao = item.find('.//nfe:xProd', ns).text
        quantidade = item.find('.//nfe:qCom', ns).text
        valor = item.find('.//nfe:vProd', ns).text

        itens.append({
            'codigo': codigo,
            'descricao': descricao,
            'quantidade': quantidade,
            'valor': valor
        })
    return itens
