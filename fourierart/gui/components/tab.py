from fourierart.utility import Nop

from PyQt5.QtWidgets import QGridLayout, QVBoxLayout

class CustomTab(QVBoxLayout):
    def __init__(self, completion_callback = Nop):
        super().__init__()

        self.completion_callback = completion_callback

        self.graph_layout = QVBoxLayout()
        self.addLayout(self.graph_layout, 1)

        self.options_layout = QGridLayout()
        self.addLayout(self.options_layout, 0)

    def on_completion(self):
        self.completion_callback()

        