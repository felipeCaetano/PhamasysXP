import xml.etree.ElementTree as ET
from xml.etree import ElementTree as ET


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


class NFeParse:
    def __init__(self):
        self.ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

    def parse_xml(self, xml_path):
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Dados básicos da nota
        nfe_data = {
            'dados_gerais': self._get_dados_gerais(root),
            'emitente': self._get_emitente(root),
            'destinatario': self._get_destinatario(root),
            'produtos': self._get_produtos(root),
            'impostos': self._get_impostos(root),
            'totais': self._get_totais(root)
        }
        return nfe_data

    def _get_dados_gerais(self, root):
        ide = root.find('.//nfe:ide', self.ns)
        if ide is not None:
            return {
                'numero': ide.findtext('nfe:nNF', namespaces=self.ns),
                'serie': ide.findtext('nfe:serie', namespaces=self.ns),
                'data_emissao': ide.findtext('nfe:dhEmi', namespaces=self.ns),
                'natureza_operacao': ide.findtext(
                    'nfe:natOp', namespaces=self.ns)
            }
        return {}

    def _get_emitente(self, root):
        emit = root.find('.//nfe:emit', self.ns)
        if emit is not None:
            return {
                'cnpj': emit.findtext('nfe:CNPJ', namespaces=self.ns),
                'nome': emit.findtext('nfe:xNome', namespaces=self.ns),
                'fantasia': emit.findtext('nfe:xFant', namespaces=self.ns),
                'ie': emit.findtext('nfe:IE', namespaces=self.ns)
            }
        return {}

    def _get_destinatario(self, root):
        dest = root.find('.//nfe:dest', self.ns)
        if dest is not None:
            return {
                'cnpj': dest.findtext('nfe:CNPJ', namespaces=self.ns),
                'nome': dest.findtext('nfe:xNome', namespaces=self.ns),
                'ie': dest.findtext('nfe:IE', namespaces=self.ns)
            }
        return {}

    def _get_produtos(self, root):
        produtos = []
        for det in root.findall('.//nfe:det', self.ns):
            prod = det.find('nfe:prod', self.ns)
            if prod is not None:
                produto = {
                    'codigo': prod.findtext('nfe:cEAN', namespaces=self.ns),
                    'descricao': prod.findtext('nfe:xProd',
                                               namespaces=self.ns),
                    'ncm': prod.findtext('nfe:NCM', namespaces=self.ns),
                    'cfop': prod.findtext('nfe:CFOP', namespaces=self.ns),
                    'unidade': prod.findtext('nfe:uCom', namespaces=self.ns),
                    'quantidade': prod.findtext(
                        'nfe:qCom', namespaces=self.ns),
                    'valor_unitario': f'{float(prod.findtext('nfe:vUnCom', namespaces=self.ns)):.2f}',
                    'valor_total': prod.findtext(
                        'nfe:vProd', namespaces=self.ns)
                }
                produtos.append(produto)
        return produtos

    def _get_impostos(self, root):
        impostos = []
        for det in root.findall('.//nfe:det', self.ns):
            imposto = det.find('nfe:imposto', self.ns)
            if imposto is not None:
                # ICMS
                icms = imposto.find('.//nfe:ICMS', self.ns)
                if icms is not None:
                    for icms_tipo in icms:
                        if icms_tipo.tag.endswith('}ICMS00'):
                            impostos.append({
                                'tipo': 'ICMS',
                                'aliquota': icms_tipo.findtext(
                                    'nfe:pICMS', namespaces=self.ns),
                                'valor': icms_tipo.findtext(
                                    'nfe:vICMS', namespaces=self.ns)
                            })

                # IPI
                ipi = imposto.find('.//nfe:IPI', self.ns)
                if ipi is not None:
                    impostos.append({
                        'tipo': 'IPI',
                        'aliquota': ipi.findtext('.//nfe:pIPI',
                                                 namespaces=self.ns),
                        'valor': ipi.findtext('.//nfe:vIPI',
                                              namespaces=self.ns)
                    })

                # PIS
                pis = imposto.find('.//nfe:PIS', self.ns)
                if pis is not None:
                    impostos.append({
                        'tipo': 'PIS',
                        'aliquota': pis.findtext('.//nfe:pPIS',
                                                 namespaces=self.ns),
                        'valor': pis.findtext('.//nfe:vPIS',
                                              namespaces=self.ns)
                    })

                # COFINS
                cofins = imposto.find('.//nfe:COFINS', self.ns)
                if cofins is not None:
                    impostos.append({
                        'tipo': 'COFINS',
                        'aliquota': cofins.findtext('.//nfe:pCOFINS',
                                                    namespaces=self.ns),
                        'valor': cofins.findtext('.//nfe:vCOFINS',
                                                 namespaces=self.ns)
                    })
        return impostos

    def _get_totais(self, root):
        total = root.find('.//nfe:total/nfe:ICMSTot', self.ns)
        if total is not None:
            return {
                'base_calculo_icms': total.findtext('nfe:vBC',
                                                    namespaces=self.ns),
                'valor_icms': total.findtext('nfe:vICMS', namespaces=self.ns),
                'valor_produtos': total.findtext('nfe:vProd',
                                                 namespaces=self.ns),
                'valor_frete': total.findtext('nfe:vFrete',
                                              namespaces=self.ns),
                'valor_seguro': total.findtext('nfe:vSeg', namespaces=self.ns),
                'valor_desconto': total.findtext('nfe:vDesc',
                                                 namespaces=self.ns),
                'valor_total': total.findtext('nfe:vNF', namespaces=self.ns)
            }
        return {}
