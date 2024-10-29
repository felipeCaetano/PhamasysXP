from kivymd.toast import toast
from kivymd.uix.button import MDFloatingActionButton, MDFlatButton
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

from services.leitura_nota_fiscal import ler_nota_fiscal


class NotasFiscaisScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "notas_fiscais"
        self.file_manager = MDFileManager(
            preview=True,
            exit_manager=self.close_file_manager,
            select_path=self.select_path,
            use_access=True
        )
        # Adiciona um rótulo de título
        self.add_widget(MDLabel(
            text="Importar Notas Fiscais",
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.8},
            font_style="H4"
        ))

        # Botão para abrir o gerenciador de arquivos
        button_open_file_manager = MDFloatingActionButton(
            icon="file-import",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            on_release=self.open_file_manager
        )
        self.add_widget(button_open_file_manager)

    def open_file_manager(self, event):
        self.file_manager.show('/')

    def select_path(self, path):
        self.close_file_manager()
        try:
            # Lê os itens da nota fiscal
            itens = ler_nota_fiscal(path)
            self.cadastrar_itens_estoque(itens)
            toast("Itens cadastrados com sucesso!")
        except Exception as e:
            # Mostra erro se houver problema
            self.show_error_dialog(str(e))

    def close_file_manager(self, *args):
        self.file_manager.close()

    def cadastrar_itens_estoque(self, itens):
        # Aqui você deve implementar a lógica para cadastrar os itens no estoque
        for item in itens:
            print(f"Código: {item['codigo']}, Descrição: {item['descricao']}, "
                  f"Quantidade: {item['quantidade']}, Valor: {item['valor']}")

    def show_error_dialog(self, error_message):
        # Exibe um diálogo de erro
        dialog = MDDialog(
            title="Erro ao importar NF-e",
            text=error_message,
            buttons=[MDFlatButton(text="Fechar",
                                  on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()