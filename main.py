from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget

from fourierart.utility import get_dark_palette
from fourierart.gui.tabs import *

class MainContents(QTabWidget):

    def __init__(self):
        super(QTabWidget, self).__init__()
        self.init()

    def on_change(self, index):
        if not self.isTabEnabled(index):
            return

        for i in range(4):
            enabled = i - index <= 1
            self.setTabEnabled(i, enabled)

        if index == 1:
            audio_segment = self.select_source.get_audio_segment()
            audio_file = AudioFile(audio_segment)
            self.quantization.set_audio(audio_file)

        if index == 2:
            audio_segment = self.select_source.get_audio_segment()
            self.spectrogram.set_audio_segment(audio_segment)

    def enable_tab(self, tab):
        self.setTabVisible(tab, True)

    def init(self):
        self.select_source = AudioSource(completion_callback=lambda: self.enable_tab(1))
        self.addTab(self.select_source, 'Select Source')

        self.quantization = Quantization(completion_callback=lambda: self.enable_tab(2))
        self.addTab(self.quantization, 'Quantization')

        self.spectrogram = Spectrogram()
        self.addTab(self.spectrogram, 'Spectrogram')

        self.export = Export()
        self.addTab(self.export, 'Export')

        self.setTabVisible(1, False)
        self.setTabVisible(2, False)
        self.setTabVisible(3, False)

        self.currentChanged.connect(self.on_change)

class App(QMainWindow):
    def set_title(self, title):
        self.title = title
        self.setWindowTitle(title)

    def set_geometry(self, left, right, top, bottom):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

        self.setGeometry(left, top, right, bottom)

    def __init__(self, title: str = 'Audio Shaper', left: int = 0, right: int = 1200, top: int = 0, bottom: int = 720):
        super(QMainWindow, self).__init__()
        
        self.set_title(title)
        self.set_geometry(left=left, right=right, top=top, bottom=bottom)

        self.main_contents = MainContents()
        self.setCentralWidget(self.main_contents)

        self.show()

if __name__ == '__main__':
    app = QApplication([])
    
    app.setStyle("Fusion")

    palette = get_dark_palette()
    app.setPalette(palette)

    ex = App()

    app.exec()