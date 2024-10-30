from kivy.uix.scrollview import ScrollView
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDFloatingActionButton, \
    MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList
from kivymd.uix.screen import MDScreen
from kivymd.uix.selectioncontrol import MDCheckbox

from custom_items.onelinecheckboxitem import OneLineCheckboxListItem
from services.leitura_nota_fiscal import ler_nota_fiscal


class NotasFiscaisScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "notas_fiscais"
        self.file_manager = MDFileManager(
            exit_manager=self.close_file_manager,
            select_path=self.select_path,
            ext=[".xml"])
        self.add_widget(
            MDLabel(
                text="Importar Notas Fiscais",
                halign="center",
                pos_hint={"center_x": 0.5, "center_y": 0.9},
                font_style="H4")
        )

        button_open_file_manager = MDFloatingActionButton(
            icon="file-import",
            pos_hint={"center_x": 0.5, "center_y": 0.8},
            on_release=self.open_file_manager
        )
        self.add_widget(button_open_file_manager)
        self.layout = MDBoxLayout(orientation="horizontal")
        self.select_all_checkbox = MDCheckbox(
            pos_hint={"center_x": 0.1, "center_y": 0.7},
            size_hint=(None, None),
            size=("48dp", "48dp")
        )
        label_for_select_all = MDLabel(
            text="Selecionar Todos",
            pos_hint={"center_x": 0.2, "center_y": 0.7})
        self.select_all_checkbox.bind(active=self.toggle_select_all)
        self.layout.add_widget(self.select_all_checkbox)
        self.layout.add_widget(label_for_select_all)
        self.scroll_view = ScrollView(
            pos_hint={"center_x": 0.5, "center_y": 0.4}, size_hint=(1, 0.6))
        self.item_list = MDList()
        self.scroll_view.add_widget(self.item_list)
        self.button_cadastrar = MDRaisedButton(
            text="Cadastrar Itens Selecionados",
            pos_hint={"center_x": 0.5, "center_y": 0.1},
            on_release=self.cadastrar_itens_selecionados
        )

    def open_file_manager(self, event):
        self.file_manager.show('/')

    def select_path(self, path):
        self.close_file_manager()
        try:
            itens = ler_nota_fiscal(path)
            self.display_items(itens)
            toast("Nota lida com sucesso!")
        except Exception as e:
            self.show_error_dialog(str(e))

    def close_file_manager(self, *args):
        self.file_manager.close()

    def display_items(self, itens):
        self.item_list.clear_widgets()
        for item in itens:
            list_item = OneLineCheckboxListItem(
                text=f"{item['codigo']} - {item['descricao']}: "
                     f"{item['quantidade']} unidades - R${item['valor']}",
            )
            list_item.item_data = item
            self.item_list.add_widget(list_item)
        self.add_widget(self.layout)
        self.add_widget(self.scroll_view)
        self.add_widget(self.button_cadastrar)

    def cadastrar_itens_selecionados(self, *args):
        selected_items = [
            item.item_data for item in self.item_list.children if
            isinstance(item, OneLineCheckboxListItem) and
            item.ids.checkbox.active]

        if not selected_items:
            toast("Nenhum item selecionado!")
            return

        # Aqui você deve implementar a lógica para cadastrar os itens no estoque
        for item in selected_items:
            print(f"Código: {item['codigo']}, Descrição: {item['descricao']}, "
                  f"Quantidade: {item['quantidade']}, Valor: {item['valor']}")

    def toggle_select_all(self, checkbox, value):
        for item in self.item_list.children:
            if isinstance(item, OneLineCheckboxListItem):
                item.ids.checkbox.active = value

    def show_error_dialog(self, error_message):
        dialog = MDDialog(
            title="Erro ao importar NF-e",
            text=error_message,
            buttons=[MDFlatButton(text="Fechar",
                                  on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()
