
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLineEdit

class CustomField(QLineEdit):
    def clear(self):
        self.setText('')

    def focusInEvent(self, event):
        super(QLineEdit, self).focusInEvent(event)

        QTimer.singleShot(0, self.clear)