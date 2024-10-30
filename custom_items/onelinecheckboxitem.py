from kivymd.uix.list import OneLineAvatarListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.lang import Builder

KV = '''
<OneLineCheckboxListItem>:
    MDCheckbox:
        id: checkbox
        size_hint: None, None
        size: "48dp", "48dp"
        pos_hint: {"center_y": .5}
        # on_active: root.checkbox_callback(root, self.active)
'''

Builder.load_string(KV)


class OneLineCheckboxListItem(OneLineAvatarListItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.checkbox_callback = checkbox_callback
