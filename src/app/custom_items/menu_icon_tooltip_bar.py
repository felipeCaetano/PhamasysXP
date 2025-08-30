from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty, BooleanProperty, DictProperty, \
    ObjectProperty


class MenuIconToolTipBar(MDBoxLayout):
    # Propriedades para ícones e tooltips
    import_icon = StringProperty("file-import")
    import_tooltip = StringProperty("Selecionar arquivo")
    clear_icon = StringProperty("cancel")
    clear_tooltip = StringProperty("Limpar campos")
    save_icon = StringProperty("content-save")
    save_tooltip = StringProperty("Salvar NFe")
    filter_icon = StringProperty("filter")
    filter_tooltip = StringProperty("Filtrar dados")
    view_icon = StringProperty("view-list")
    view_tooltip = StringProperty("Alterar visualização")

    # Propriedades de visibilidade
    show_import = BooleanProperty(True)
    show_clear = BooleanProperty(True)
    show_save = BooleanProperty(True)
    show_filter = BooleanProperty(True)
    show_view = BooleanProperty(True)
    show_divider = BooleanProperty(True)

    on_import = ObjectProperty(None)
    on_clear = ObjectProperty(None)
    on_save = ObjectProperty(None)

    # Dicionário para armazenar referências aos botões
    buttons = DictProperty({})

    def __init__(self, **kwargs):
        self.register_event_type('on_import_press')
        self.register_event_type('on_clear_press')
        self.register_event_type('on_save_press')
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = "16dp"
        self.padding = ["16dp", "0dp"]

    def on_import_press(self, *args):
        """Evento disparado quando o botão de importar é pressionado"""
        if self.on_import:
            self.on_import()

    def on_clear_press(self, *args):
        """Evento disparado quando o botão de limpar é pressionado"""
        if self.on_clear:
            self.on_clear()

    def on_save_press(self, *args):
        """Evento disparado quando o botão de salvar é pressionado"""
        if self.on_save:
            self.on_save()

    def on_filter_press(self, *args):
        """Evento disparado quando o botão de filtro é pressionado"""
        if self.on_filter:
            self.on_filter()

    def on_view_press(self, *args):
        """Evento disparado quando o botão de visualização é pressionado"""
        if self.on_view:
            self.on_view()

    def toggle_button(self, button_name, show=None):
        """
        Alterna ou define a visibilidade de um botão específico
        :param button_name: Nome do botão ('import', 'clear', 'save', 'filter', 'view')
        :param show: Se None, alterna o estado. Se True/False, define o estado
        """
        prop_name = f'show_{button_name}'
        if hasattr(self, prop_name):
            if show is None:
                setattr(self, prop_name, not getattr(self, prop_name))
            else:
                setattr(self, prop_name, show)

    def show_all_buttons(self):
        """Mostra todos os botões"""
        self.show_import = True
        self.show_clear = True
        self.show_save = True
        self.show_filter = True
        self.show_view = True
        self.show_divider = True

    def hide_all_buttons(self):
        """Esconde todos os botões"""
        self.show_import = False
        self.show_clear = False
        self.show_save = False
        self.show_filter = False
        self.show_view = False
        self.show_divider = False