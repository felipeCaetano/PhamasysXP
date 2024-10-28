import xml.etree.ElementTree as ET


def ler_nota_fiscal(file_path):
    itens = []

    tree = ET.parse(file_path)
    root = tree.getroot()

    ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

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
