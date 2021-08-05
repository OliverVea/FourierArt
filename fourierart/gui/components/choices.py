from fourierart.utility import Nop
from fourierart.gui.primitives import Choice

from PyQt5.QtWidgets import QComboBox, QGroupBox, QHBoxLayout

class OptionChoice(QGroupBox):
    def __init__(self, title, choice: Choice, callback=Nop):
        super().__init__()

        self.choice = choice
        self.callback = callback

        # Layout
        self.setTitle(title)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Initialize dropdown
        self.dropdown = QComboBox()
        self.dropdown.addItems(choice.keys)
        self.dropdown.currentTextChanged.connect(self.callback)
        self.layout.addWidget(self.dropdown)
