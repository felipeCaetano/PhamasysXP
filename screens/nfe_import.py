from kivy.metrics import dp
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.tab import MDTabsBase, MDTabs
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import OneLineListItem
import os

from services.leitura_nota_fiscal import NFeParse

# Interface em KV Language
KV = '''
MDBoxLayout:
    orientation: 'vertical'
    spacing: '10dp'

    MDTopAppBar:
        title: "Importação de NF-e"
        left_action_items: [["arrow-left", lambda x: app.voltar_tela_principal()]]
        right_action_items: [["close", lambda x: root.parent.limpar_notas()]]

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


# class ImportScreen(Screen):
#     pass


# class PreviewDialog(MDBoxLayout):
#     pass


class NFEScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            ext=[".xml"]
        )
        self.selected_rows = []
        self.nfe_parser = NFeParse()

    def on_enter(self):
        layout = Builder.load_string(KV)
        if layout:
            self.clear_widgets()
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
            app.show_dialog("Erro ao processar arquivo", str(e))
            print(e)

    def mostrar_dados_nfe(self, nfe_data):
        self.import_screen: MDTabs = self.children[0].ids.tabs
        if not nfe_data:
            return
        if tabs := self.import_screen.get_tab_list():
            for tab in tabs:
                self.import_screen.clear_widgets(tab)
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
            # tab.ids.container.clear_widgets()
            if isinstance(data, list):
                if title == 'Produtos':
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
        data_table = MDDataTable(
            use_pagination=True,
            size_hint=(1, None),
            height=dp(450),
            column_data=[
                ("Código", dp(30)), ("Descrição", dp(65)), ('NCM', dp(20)),
                ('CFOP', dp(20)), ('Unidade', dp(20)),
                ("Quantidade", dp(20)), ("valor unit.", dp(30)),
                ("Valor", dp(30)),
            ],
            row_data=[(
                item['codigo'], item['descricao'], item['ncm'], item['cfop'],
                item['unidade'], item['quantidade'],
                item["valor_unitario"], item['valor_total']) for item
                in
                data],
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
