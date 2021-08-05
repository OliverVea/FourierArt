from PyQt5.QtWidgets import QComboBox, QGroupBox, QHBoxLayout

class OptionChoice(QGroupBox):
    def __init__(self, title, choices: dict = {}):
        super().__init__()

        self.setTitle(title)

        self.dropdown = QComboBox()
        self.dropdown.addItems(list(choices.keys()))

        self.dropdown.currentTextChanged.connect(self.callback)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.dropdown)

        self.setLayout(self.layout)

        self.choices = choices

    def callback(self, text):
        for fn in self.callbacks:
            fn(self.choices[text])