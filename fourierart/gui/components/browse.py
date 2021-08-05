from fourierart import Callback
from fourierart.utility import get_file_name

from PyQt5.QtWidgets import QHBoxLayout, QLineEdit, QPushButton
from os.path import exists

class CustomBrowse(QHBoxLayout):
    def __init__(self):
        super().__init__()

        self.file = None
        self.callback = Callback()

        self.field = QLineEdit('Press \'Browse\' to select file.')
        self.field.setReadOnly(True)
        self.addWidget(self.field)

        self.button = QPushButton('Browse')
        self.button.clicked.connect(self.select_file)
        self.addWidget(self.button)

    def select_file(self, *args):
        file = get_file_name()

        if file == '' or not exists(file):
            return

        self.file = file
        self.field.setText(file)
        self.callback()

    def connect(self, callback):
        self.callback.register(callback)     
