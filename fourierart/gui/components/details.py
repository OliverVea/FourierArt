
from PyQt5.QtWidgets import QLabel, QVBoxLayout

class Detail:
    def __init__(self, key, value, format = None):
        self.key = key
        self.value = value
        self.format = format
        self.label = QLabel()

    def update(self, value):
        self.value = value
        self.label.setText(self.format(self.value))

class CustomDetails(QVBoxLayout):
    def __init__(self, details: list[Detail]):
        super().__init__()

        self.details = {detail.key: detail for detail in details}

        for detail in details:
            self.addWidget(detail.label)
            detail.update(detail.value)

    def update(self, details):
        # TODO: do this smarter.
        for detail in details:
            if detail.key in self.details:
                self.details[detail.key].update(detail.value)