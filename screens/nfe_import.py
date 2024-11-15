from kivy.metrics import dp
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import OneLineListItem
import xml.etree.ElementTree as ET
import os
from datetime import datetime

# Interface em KV Language
KV = '''
MDBoxLayout:
    orientation: 'vertical'
    spacing: '10dp'

    MDTopAppBar:
        title: "Importação de NF-e"
        left_action_items: [["arrow-left", lambda x: app.voltar_tela_principal()]]

    MDBoxLayout:
        orientation: 'vertical'
        spacing: '10dp'
        padding: '10dp'

        MDCard:
            orientation: 'vertical'
            padding: '8dp'
            size_hint: None, None
            size: "300dp", "100dp"
            pos_hint: {"center_x": .5}

            MDLabel:
                text: "Selecione o arquivo XML da NF-e"
                halign: "center"

            MDRaisedButton:
                text: "Escolher Arquivo"
                pos_hint: {"center_x": .5}
                on_release: root.parent.abrir_gerenciador_arquivos()

        MDTabs:
            id: tabs

<Tab>
    MDBoxLayout:
        orientation: 'vertical'
        padding: '10dp'
        spacing: '10dp'

        MDScrollView:
            MDList:
                id: container

<PreviewDialog>:
    orientation: 'vertical'
    spacing: '10dp'
    padding: '10dp'
    size_hint_y: None
    height: "400dp"

    MDScrollView:
        MDList:
            id: preview_list
'''


class Tab(MDFloatLayout, MDTabsBase):
    pass


class ImportScreen(Screen):
    pass


class PreviewDialog(MDBoxLayout):
    pass


class NFEScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            ext=[".xml"]
        )
        self.nfe_parser = NFeParse()


    def on_enter(self):
        layout = Builder.load_string(KV)
        if layout:
            self.add_widget(layout)
        else:
            print("Erro: Não foi possível carregar o layout KV.")

    def abrir_gerenciador_arquivos(self):
        self.file_manager.show(os.path.expanduser("~"))

    def exit_manager(self, *args):
        self.file_manager.close()

    def select_path(self, path):
        self.file_manager.close()
        try:
            nfe_data = self.nfe_parser.parse_xml(path)
            self.mostrar_dados_nfe(nfe_data)
        except Exception as e:
            app = MDApp.get_running_app()
            # app.show_dialog("Erro ao processar arquivo", str(e))
            print(e)

    def mostrar_dados_nfe(self, nfe_data):
        self.import_screen = self.children[0].ids.tabs
        if not nfe_data:
            return
        if self.import_screen.get_tab_list():
            self.import_screen.clear_widgets()

        # Cria tabs para cada seção
        sections = {
             'Dados Gerais': nfe_data['dados_gerais'],
             'Emitente': nfe_data['emitente'],
             'Destinatário': nfe_data['destinatario'],
             'Produtos': nfe_data['produtos'],
             'Impostos': nfe_data['impostos'],
             'Totais': nfe_data['totais']
         }
        for title, data in sections.items():
            tab = Tab(title=title)
            if isinstance(data, list):
                if title=='Produtos':
                    tab.ids.container.add_widget(
                        self._create_data_table(data)
                    )
                else:
                    for item in data:
                        for key, value in item.items():
                            tab.ids.container.add_widget(
                                OneLineListItem(text=f"{key}: {value}")
                            )
            else:
                for key, value in data.items():
                    tab.ids.container.add_widget(
                        OneLineListItem(text=f"{key}: {value}")
                    )

            self.import_screen.add_widget(tab)

    def _create_data_table(self, data):
        [print(item) for item in data]
        data_table = MDDataTable(
            use_pagination=True,
            size_hint=(1, None),
            height=dp(450),
            column_data=[
                ("Código", dp(40)), ("Descrição", dp(65)), ('NCM', dp(30)),
                ('CFOP', dp(30)), ('Unidade', dp(30)),
                ("Quantidade", dp(20)), ("valor unit.", dp(30)),
                ("Valor", dp(30)),
            ],
            row_data=[(
                item['codigo'], item['descricao'], item['ncm'], item['cfop'],
                item['unidade'], item['quantidade'],
                item["valor_unitario"], item['valor_total']) for item in data],
            check=True
        )
        data_table.bind(on_check_press=self.on_check_press)
        return data_table

    def on_check_press(self, instance_table, current_row):
        '''Called when a table row is clicked.'''
        if current_row in self.selected_rows:
            self.selected_rows.remove(current_row)
        else:
            self.selected_rows.append(current_row)
        print(self.selected_rows)

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
                'natureza_operacao': ide.findtext('nfe:natOp',
                                                  namespaces=self.ns)
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
                    'codigo': prod.findtext('nfe:cProd', namespaces=self.ns),
                    'descricao': prod.findtext('nfe:xProd', namespaces=self.ns),
                    'ncm': prod.findtext('nfe:NCM', namespaces=self.ns),
                    'cfop': prod.findtext('nfe:CFOP', namespaces=self.ns),
                    'unidade': prod.findtext('nfe:uCom', namespaces=self.ns),
                    'quantidade': prod.findtext('nfe:qCom', namespaces=self.ns),
                    'valor_unitario': prod.findtext('nfe:vUnCom',
                                                    namespaces=self.ns),
                    'valor_total': prod.findtext('nfe:vProd',
                                                 namespaces=self.ns)
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
                                'aliquota': icms_tipo.findtext('nfe:pICMS',
                                                               namespaces=self.ns),
                                'valor': icms_tipo.findtext('nfe:vICMS',
                                                            namespaces=self.ns)
                            })

                # IPI
                ipi = imposto.find('.//nfe:IPI', self.ns)
                if ipi is not None:
                    impostos.append({
                        'tipo': 'IPI',
                        'aliquota': ipi.findtext('.//nfe:pIPI',
                                                 namespaces=self.ns),
                        'valor': ipi.findtext('.//nfe:vIPI', namespaces=self.ns)
                    })

                # PIS
                pis = imposto.find('.//nfe:PIS', self.ns)
                if pis is not None:
                    impostos.append({
                        'tipo': 'PIS',
                        'aliquota': pis.findtext('.//nfe:pPIS',
                                                 namespaces=self.ns),
                        'valor': pis.findtext('.//nfe:vPIS', namespaces=self.ns)
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
                'valor_frete': total.findtext('nfe:vFrete', namespaces=self.ns),
                'valor_seguro': total.findtext('nfe:vSeg', namespaces=self.ns),
                'valor_desconto': total.findtext('nfe:vDesc',
                                                 namespaces=self.ns),
                'valor_total': total.findtext('nfe:vNF', namespaces=self.ns)
            }
        return {}

# class NFeImportApp(MDApp):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.file_manager = MDFileManager(
#             exit_manager=self.exit_manager,
#             select_path=self.select_path
#         )
#         self.nfe_parser = NFeParse()
#         self.current_nfe_data = None
#
#     def build(self):
#         Builder.load_string(KV)
#         self.import_screen = ImportScreen(name='import')
#         return self.import_screen
#
#     def abrir_gerenciador_arquivos(self):
#         self.file_manager.show(os.path.expanduser("~"))
#
#     def exit_manager(self, *args):
#         self.file_manager.close()
#
#     def select_path(self, path):
#         self.file_manager.close()
#         try:
#             self.current_nfe_data = self.nfe_parser.parse_xml(path)
#             self.mostrar_dados_nfe()
#         except Exception as e:
#             self.show_error_dialog("Erro ao processar arquivo", str(e))
#
#     def mostrar_dados_nfe(self):
#         if not self.current_nfe_data:
#             return
#
#         # Limpa as tabs existentes
#         self.import_screen.ids.tabs.clear_widgets()
#
#         # Cria tabs para cada seção
#         sections = {
#             'Dados Gerais': self.current_nfe_data['dados_gerais'],
#             'Emitente': self.current_nfe_data['emitente'],
#             'Destinatário': self.current_nfe_data['destinatario'],
#             'Produtos': self.current_nfe_data['produtos'],
#             'Impostos': self.current_nfe_data['impostos'],
#             'Totais': self.current_nfe_data['totais']
#         }
#
#         for title, data in sections.items():
#             tab = Tab(title=title)
#             if isinstance(data, list):
#                 for item in data:
#                     for key, value in item.items():
#                         tab.ids.container.add_widget(
#                             OneLineListItem(text=f"{key}: {value}")
#                         )
#             else:
#                 for key, value in data.items():
#                     tab.ids.container.add_widget(
#                         OneLineListItem(text=f"{key}: {value}")
#                     )
#
#             self.import_screen.ids.tabs.add_widget(tab)
#
#     def show_error_dialog(self, title, text):
#         dialog = MDDialog(
#             title=title,
#             text=text,
#             buttons=[
#                 MDFlatButton(
#                     text="OK",
#                     on_release=lambda x: dialog.dismiss()
#                 )
#             ]
#         )
#         dialog.open()
#
#     def voltar_tela_principal(self):
#         # Implementar a navegação de volta
#         pass
#
#
# if __name__ == '__main__':
#     NFeImportApp().run()
