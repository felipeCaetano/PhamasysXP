from kivy.uix.scrollview import ScrollView
from kivymd.material_resources import dp
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDFloatingActionButton, \
    MDRaisedButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField

from custom_items.vendorcard import VendorCard
from services.leitura_nota_fiscal import ler_nota_fiscal


class NotasFiscaisScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_rows = []
        self.data_table = None
        self.name = "notas_fiscais"
        self.file_manager = MDFileManager(
            exit_manager=self.close_file_manager,
            select_path=self.select_path,
            ext=[".xml"])
        self.top_layout = MDBoxLayout(
            orientation="vertical",
            padding=(10, 10, 10, 0),
            size_hint=(1, None),
            height=dp(120)
        )
        self.top_layout.add_widget(
            MDLabel(
                text="Importar Notas Fiscais",
                halign="center",
                font_style="H4"
            )
        )
        button_open_file_manager = MDFloatingActionButton(
            icon="file-import",
            pos_hint={"center_x": 0.5},
            on_release=self.open_file_manager
        )
        self.top_layout.add_widget(button_open_file_manager)
        self.main_layout = MDBoxLayout(
            orientation="vertical", spacing=10, padding=10
        )
        self.main_layout.add_widget(self.top_layout)

        self.vendor_card = VendorCard(opacity=0)
        # self.vendor_card.cadastrar_fornecedor = self.cadastrar_fornecedor
        self.main_layout.add_widget(self.vendor_card)
        self.scroll_view = ScrollView(size_hint=(1, 0.5))
        self.main_layout.add_widget(self.scroll_view)
        self.button_cadastrar = MDRaisedButton(
            text="Cadastrar Itens Selecionados",
            pos_hint={"center_x": 0.5, "center_y": 0.1},
            on_release=self.cadastrar_itens_selecionados,
            opacity=0
        )
        self.main_layout.add_widget(self.button_cadastrar)
        self.add_widget(self.main_layout)

    def open_file_manager(self, event):
        self.file_manager.show('/')

    def select_path(self, path):
        self.close_file_manager()
        try:
            fornecedor, itens = ler_nota_fiscal(path)
            self.display_fornecedor(fornecedor)
            self.display_items(itens)
            toast("Nota lida com sucesso!")
        except Exception as e:
            self.show_error_dialog(str(e))

    def close_file_manager(self, *args):
        self.file_manager.close()

    def display_fornecedor(self, fornecedor):
        """Exibe os dados do fornecedor."""
        self.vendor_card.cnpj = fornecedor[0]['cnpj']
        self.vendor_card.nome = fornecedor[0]['nome']
        self.vendor_card.nome_fantasia = fornecedor[0]['nome_fantasia']
        self.vendor_card.telefone = fornecedor[0]['telefone']
        self.vendor_card.cadastrar_fornecedor = self.cadastrar_fornecedor
        self.vendor_card.opacity = 1

    def display_items(self, itens):
        """ Exibe os itens da nota fiscal na MDDataTable."""
        if self.data_table:
            self.scroll_view.remove_widget(self.data_table)
        self.data_table = MDDataTable(
            use_pagination=True,
            size_hint=(1, None),
            height=dp(450),
            column_data=[
                ("Código", dp(40)), ("Descrição", dp(65)),
                ("Quantidade", dp(20)), ("valor unit.", dp(30)),
                ("Valor", dp(30)),
            ],
            row_data=[(
                item['codigo'], item['descricao'], item['quantidade'],
                item["valor unit"], item['valor']) for item in itens],
            check=True
        )
        self.data_table.bind(on_check_press=self.on_check_press)
        self.scroll_view.add_widget(self.data_table)
        self.button_cadastrar.opacity = 1

    def on_check_press(self, instance_table, current_row):
        '''Called when a table row is clicked.'''
        if current_row in self.selected_rows:
            self.selected_rows.remove(current_row)
        else:
            self.selected_rows.append(current_row)
        print(self.selected_rows)

    def cadastrar_fornecedor(self, event):
        field_list = reversed(self.vendor_card.children[0].children)
        dados_fornecedor = [field.text for field in field_list if
                            isinstance(field, MDTextField)]
        # Aqui você deve implementar a lógica para cadastrar os fornecedores
        toast("Fornecedor Cadastrado com sucesso!")

    def cadastrar_itens_selecionados(self, *args):
        if not self.selected_rows:
            toast("Nenhum item selecionado!")
            return
        # Aqui você deve implementar a lógica para cadastrar os itens no estoque
        for item in self.selected_rows:
            print(item)

    def show_error_dialog(self, error_message):
        dialog = MDDialog(
            title="Erro ao importar NF-e",
            text=error_message,
            buttons=[MDFlatButton(text="Fechar",
                                  on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()
