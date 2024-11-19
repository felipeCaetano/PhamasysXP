import os

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.tab import MDTabsBase, MDTabs
from kivymd.uix.tab.tab import MDTabsException  # noinspection PyProtectedMember
from kivymd.uix.textfield import MDTextField
from kivymd.uix.tooltip import MDTooltip

from services.leitura_nota_fiscal import NFeParse

KV = '''
MDBoxLayout:
    orientation: 'vertical'
    spacing: '10dp'

    MDTopAppBar:
        title: "Importação de NF-e"
        left_action_items: [["arrow-left", lambda x: root.parent.back_to_main_screen()]]
        right_action_items: [["menu", lambda x: root.parent.limpar_notas()]]

    MDBoxLayout:
        orientation: 'vertical'
        spacing: '10dp'
        padding: '10dp'

        MDCard:
            orientation: 'horizontal'
            padding: '8dp'
            size_hint: 1, None
            height: "56dp"
            md_bg_color: app.theme_cls.bg_light
            elevation: 1
            
            MDBoxLayout:
                orientation: 'horizontal'
                spacing: "16dp"   # Espaçamento entre botões
                padding: ["16dp", "0dp"]  # Padding nas laterais
                
                TooltipMDIconButton:
                    icon: "file-import"
                    tooltip_text: "Selecionar arquivo"
                    on_release: root.parent.abrir_gerenciador_arquivos()
                    
                TooltipMDIconButton:
                    icon: "cancel"
                    tooltip_text: "Limpar campos"
                    on_release: root.parent.limpar_notas()

                TooltipMDIconButton:
                    icon: "content-save"
                    tooltip_text: "Salvar NFe"
                    on_release: root.parent.salvar_nfe()
                    
                MDWidget:
                    size_hint_x: None
                    width: "1dp"
                    md_bg_color: app.theme_cls.divider_color
                
                # Botões de visualização/filtro
                TooltipMDIconButton:
                    icon: "filter"
                    tooltip_text: "Filtrar dados"
                    on_release: root.parent.mostrar_filtros()
                
                TooltipMDIconButton:
                    icon: "view-list"
                    tooltip_text: "Alterar visualização"
                    on_release: root.parent.alterar_visualizacao()
            
            Widget:  # Espaçador flexível
                size_hint_x: 1

        MDTabs:
            id: tabs
        MDRaisedButton:
            id: button_cadastrar
            text: "Cadastrar Itens Selecionados"
            pos_hint: {"center_x": 0.5, "center_y": 0.1}
            on_press: root.parent.cadastrar_itens_selecionados()
            opacity: 0

<Tab>
    MDBoxLayout:
        orientation: 'vertical'
        padding: '10dp'
        spacing: '10dp'

        MDScrollView:
            MDList:
                id: container

<TooltipMDIconButton@MDIconButton+MDTooltip>:
    shift_y: dp(25)
    icon_size: "24dp"
    theme_icon_color: "Custom"
    icon_color: app.theme_cls.primary_color
    

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


class EditableField(MDBoxLayout):
    def __init__(self, key, value, callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.adaptive_height = True
        self.spacing = 10
        self.padding = [dp(5), 0, dp(5), 0]

        # Label do campo
        self.key = key
        self.field_label = MDLabel(
            text=f"{key}:",
            size_hint_x=0.1,
            bold=True,
            halign='center',
            padding=[0,0,dp(5),0],
        )

        # Campo de texto editável
        self.text_field = MDTextField(text=str(value), size_hint_x=0.2)
        # Botões de ação
        self.edit_button = MDIconButton(icon="pencil", size_hint_x=0.1,
                                        on_release=self.toggle_edit)
        self.add_widget(self.field_label)
        self.add_widget(self.text_field)
        self.add_widget(self.edit_button)

        self.text_field.disabled = True
        self.callback = callback

    def toggle_edit(self, *args):
        if self.text_field.disabled:
            # Habilita edição
            self.text_field.disabled = False
            self.edit_button.icon = "content-save"
            self.text_field.focus = True
        else:
            # Salva as alterações
            self.text_field.disabled = True
            self.edit_button.icon = "pencil"
            if self.callback:
                self.callback(self.key, self.text_field.text)


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

    def limpar_notas(self):
        """Limpa todas as notas fiscais abertas"""
        self.selected_rows.clear()
        for tab in self.children[0].ids.tabs.get_tab_list():
            try:
                self.children[0].ids.tabs.remove_widget(tab)
                # self.nfe_tabs.clear()
            except AttributeError:
                self.back_to_main_screen()
            # except MDTabsException:
            #     self.back_to_main_screen()
        self.children[0].ids.button_cadastrar.opacity = 0

    def back_to_main_screen(self):
        app = MDApp.get_running_app()
        app.sm.current = 'main'

    def mostrar_dados_nfe(self, nfe_data):
        self.import_screen: MDTabs = self.children[0].ids.tabs
        self.btn_cadastrar = self.children[0].ids.button_cadastrar
        if not nfe_data:
            return
        for tab in self.import_screen.get_tab_list():
            self.import_screen.remove_widget(tab)
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
            if title == 'Produtos':
                tab.ids.container.add_widget(self._create_data_table(data))
            else:
                if isinstance(data, list):
                    for item in data:
                        card = MDCard(
                            orientation='vertical',
                            size_hint_y=None,
                            height=self._calculate_card_height(item),
                            padding=dp(10),
                            spacing=dp(5),
                            md_bg_color=[0.9, 0.9, 0.9, 1]
                        )
                        for key, value in item.items():
                            card.add_widget(
                                MDTextField(
                                    hint_text=f"{key}",
                                    text=f"{value}")
                            )
                        tab.ids.container.add_widget(card)
                else:
                    layout = MDGridLayout(cols=len(data) // 2, spacing=dp(2))
                    for key, value in data.items():
                        layout.add_widget(
                            EditableField(
                                key=key.capitalize(),
                                value=value,
                                callback=None
                            )
                        )
                    tab.ids.container.add_widget(layout)
            Clock.schedule_once(self._send_toast, 2)
            self.import_screen.add_widget(tab)
            self.btn_cadastrar.opacity = 1

    def cadastrar_itens_selecionados(self, *args):
        if not self.selected_rows:
            toast("Nenhum item selecionado!")
            return
        # Aqui você deve implementar a lógica para cadastrar os itens no estoque
        for item in self.selected_rows:
            print(item)

    def mostrar_filtros(self, *args):
        # Implementar lógica de filtros
        pass

    def alterar_visualizacao(self, *args):
        # Implementar troca de visualização
        pass

    def mostrar_ajuda(self, *args):
        # Mostrar diálogo de ajuda
        pass

    def salvar_nfe(self, *args):
        pass

    def _calculate_card_height(self, item_data):
        """Calcula a altura necessária para o card baseado no número de campos"""
        base_height = dp(20)  # Padding
        field_height = dp(60)  # Altura estimada por campo
        title_height = dp(30)  # Altura do título
        return base_height + (len(item_data) * field_height) + title_height

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

    def _send_toast(self, *args):
        toast("Nota lida com sucesso!")

    def on_check_press(self, instance_table, current_row):
        """Called when a table row is clicked."""
        if current_row in self.selected_rows:
            self.selected_rows.remove(current_row)
        else:
            self.selected_rows.append(current_row)
        print(self.selected_rows)
