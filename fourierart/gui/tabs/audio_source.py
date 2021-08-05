from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QLineEdit, QTabWidget, QVBoxLayout, QWidget, QLabel, QPushButton
from PyQt5.QtCore import QTimer, Qt

from qtrangeslider import QRangeSlider

from os.path import basename

from fourierart.audio.audio_file import AudioFile
from fourierart.utility import get_file_name
from fourierart.gui.plots.audio_file_overview import AudioFileOverview

from pydub.playback import play

class BrowseAudio(QWidget):
    def __init__(self, graph_view, time_selection_bar, enable_tab):
        super(QWidget, self).__init__()

        self.audio_file = None
        self.enable_tab = enable_tab

        self.graph_view = graph_view
        self.time_selection_bar = time_selection_bar

        self.layout = QVBoxLayout()

        self.box = QLineEdit('Press \'Browse\' to select audio files.')
        self.box.setReadOnly(True)
        self.button = QPushButton('Browse')

        browseLayout = QHBoxLayout()

        browseLayout.addWidget(self.box, 1)
        browseLayout.addWidget(self.button, 0)

        detailsLayout = QGridLayout()

        self.filename = QLabel('')
        self.duration = QLabel('')
        self.channels = QLabel('')
        self.fs = QLabel('')
        self.bit_depth = QLabel('')

        self.set_details('', '', '', '', '')

        detailsLayout.addWidget(self.filename)
        detailsLayout.addWidget(self.duration)
        detailsLayout.addWidget(self.channels)
        detailsLayout.addWidget(self.fs)
        detailsLayout.addWidget(self.bit_depth)

        self.button.clicked.connect(self.select_file)

        self.layout.addLayout(browseLayout, 0)
        self.layout.addLayout(detailsLayout)

        self.setLayout(self.layout)

    def set_details(self, filename, fs, duration, channels, bit_depth):
        self.filename.setText(f'Filename: {filename}')
        self.duration.setText(f'Duration: {duration}')
        self.channels.setText(f'Channels: {channels}')
        self.fs.setText(f'Sample rate: {fs}')
        self.bit_depth.setText(f'Bit depth: {bit_depth}')

    def select_file(self, state):
        file = get_file_name(self)

        if file == '':
            return

        self.box.setText(file)

        self.audio_file = AudioFile.from_file(file)

        self.graph_view.set_audio(self.audio_file)

        self.set_details(
            basename(file), 
            f'{self.audio_file.fs:,} Hz', 
            f'{self.audio_file.t:.1f} s', 
            self.audio_file.c, 
            f'{self.audio_file.w * 8} bit'
        )

        self.time_selection_bar.setMaximum(self.audio_file.n)
        self.time_selection_bar.setValue((0, self.audio_file.n))

        self.enable_tab()

    def set_time(self, start, end):
        self.start = start
        self.end = end
        
        self.graph_view.set_audio(self.audio_file, start, end)

class AudioSource(QWidget):
    def __init__(self, enable_tab, bar_b_max: int = 1000):
        super(QWidget, self).__init__()

        self.layout = QVBoxLayout()

        self.browse_audio = None
        self.bar_b_max = bar_b_max
        self.enable_tab = enable_tab

        # Graph part
        self.graph_layout = QVBoxLayout()
        self.graph_view = AudioFileOverview()
        self.graph_layout.addWidget(self.graph_view, 1)

        self.graph_options_layout = QHBoxLayout()

        self.bars_layout = QVBoxLayout()

        self.time_selection_bar_A = QRangeSlider(Qt.Horizontal)
        self.time_selection_bar_B = QRangeSlider(Qt.Horizontal)

        self.time_selection_bar_A.sliderMoved.connect(self.on_slider_change)
        self.time_selection_bar_B.sliderMoved.connect(self.on_slider_change)
        
        self.time_selection_bar_A.setMaximum(1)
        self.time_selection_bar_A.setValue((0, 1))
        self.time_selection_bar_B.setMaximum(bar_b_max)
        self.time_selection_bar_B.setValue((0, bar_b_max))

        self.play_button = QPushButton('Play')
        self.play_button.clicked.connect(self.on_click_play)

        self.bars_layout.addWidget(self.time_selection_bar_A)
        self.bars_layout.addWidget(self.time_selection_bar_B)

        self.graph_options_layout.addLayout(self.bars_layout, 1)
        self.graph_options_layout.addWidget(self.play_button, 0)
        
        self.graph_layout.addLayout(self.graph_options_layout, 0)

        self.layout.addLayout(self.graph_layout, 1)

        # Source selection part
        self.source_tab = QTabWidget()
        self.source_tab.setTabPosition(2)
        self.browse_audio = BrowseAudio(self.graph_view, self.time_selection_bar_A, enable_tab)
        self.source_tab.addTab(self.browse_audio, 'Audio File')

        self.layout.addWidget(self.source_tab)

        self.setLayout(self.layout)

    def get_audio_segment(self):
        start, end = self.read_range_bars()

        t = self.browse_audio.audio_file.t * 1000
        t_start, t_end = int(t * start), int(t * end)

        return self.browse_audio.audio_file.audio_segment[t_start:t_end]

    def on_click_play(self, state):
        audio_segment = self.get_audio_segment()

        audio_segment = audio_segment.set_frame_rate(44100)
        audio_segment = audio_segment.set_sample_width(2)

        play(audio_segment)

    def read_range_bars(self):
        n = self.browse_audio.audio_file.n

        a_min, a_max = self.time_selection_bar_A.value()
        b_min, b_max = self.time_selection_bar_B.value()

        a_min, a_max = a_min / n, a_max / n
        b_min, b_max = b_min / self.bar_b_max, b_max / self.bar_b_max

        start, end = (a_max - a_min) * b_min + a_min, (a_max - a_min) * b_max + a_min

        return (start, end)


    def on_slider_change(self, value):
        # Check if audio file is even loaded
        if not self.browse_audio or not self.browse_audio.audio_file:
            return

        a_min, a_max = self.time_selection_bar_A.value()
        b_min, b_max = self.time_selection_bar_B.value()

        if abs(a_max - a_min) < 10:
            return

        if abs(b_max - b_min) < 10:
            return
        
        start, end = self.read_range_bars()

        self.browse_audio.set_time(start, end)
