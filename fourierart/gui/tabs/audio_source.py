from fourierart import Callback
from fourierart.audio.audio_file import AudioFile
from fourierart.gui.components import CustomTab, CustomBrowse, CustomDetails, Detail
from fourierart.gui.plots.audio_file_overview import AudioFileOverview

from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from qtrangeslider import QRangeSlider
from os.path import basename
from pydub.playback import play

class AudioSource(CustomTab):
    def __init__(self, completion_callback: Callback = Callback(), bar_b_max: int = 1000):
        super().__init__(completion_callback=completion_callback)

        self.audio_file = None
        self.bar_b_max = bar_b_max

        # Setting up the layout
        self.graph_view = AudioFileOverview()
        self.graph_layout.addWidget(self.graph_view, 1)

        self.graph_options_layout = QHBoxLayout()
        self.graph_layout.addLayout(self.graph_options_layout, 0)

        self.bars_layout = QVBoxLayout()
        self.graph_options_layout.addLayout(self.bars_layout, 1)

        # Upper timeline bar
        self.time_selection_a = QRangeSlider(Qt.Horizontal)
        self.time_selection_a.sliderMoved.connect(self.on_slider_change)
        self.time_selection_a.setMaximum(1)
        self.time_selection_a.setValue((0, 1))
        self.bars_layout.addWidget(self.time_selection_a)

        # Lower timeline bar
        self.time_selection_b = QRangeSlider(Qt.Horizontal)
        self.time_selection_b.sliderMoved.connect(self.on_slider_change)
        self.time_selection_b.setMaximum(bar_b_max)
        self.time_selection_b.setValue((0, bar_b_max))
        self.bars_layout.addWidget(self.time_selection_b)

        # Play button
        self.play_button = QPushButton('Play')
        self.play_button.clicked.connect(self.on_click_play)
        self.graph_options_layout.addWidget(self.play_button, 0)

        # Source selection part
        self.browse = CustomBrowse()
        self.browse.connect(self.on_file_selected)
        self.options_layout.addLayout(self.browse, 0, 0, 1, 2)

        # Details
        self.details = CustomDetails([
            Detail(key='filename', value='', format=lambda x: f'Filename: {x}'),
            Detail(key='duration', value='', format=lambda x: f'Duration: {x}'),
            Detail(key='channels', value='', format=lambda x: f'Channels: {x}'),
            Detail(key='fs', value='', format=lambda x: f'Sample rate: {x}'),
            Detail(key='bit_depth', value='', format=lambda x: f'Bit depth: {x}'),
        ])
        self.options_layout.addLayout(self.details, 1, 0, 1, 2)

    def on_file_selected(self):
        file = self.browse.file
        self.audio_file = AudioFile.from_file(file)

        self.graph_view.set_audio(self.audio_file)

        self.details.update([
            Detail(key='filename', value=basename(file)),
            Detail(key='duration', value=f'{self.audio_file.fs:,} Hz'),
            Detail(key='channels', value=f'{self.audio_file.t:.1f} s'),
            Detail(key='fs', value=f'{self.audio_file.c}'),
            Detail(key='bit_depth', value=f'{self.audio_file.w * 8} bit'),
        ])

        self.time_selection_a.setMaximum(self.audio_file.n)
        self.time_selection_a.setValue((0, self.audio_file.n))
        self.time_selection_b.setValue((0, self.bar_b_max))

        self.on_completion()

    def on_click_play(self, state):
        start, end = self.read_range_bars()

        audio_segment = self.audio_file.get_segment(start, end)

        audio_segment = audio_segment.set_frame_rate(44100)
        audio_segment = audio_segment.set_sample_width(2)

        play(audio_segment)

    def read_range_bars(self):
        n = self.audio_file.n

        a_min, a_max = self.time_selection_a.value()
        b_min, b_max = self.time_selection_b.value()

        a_min, a_max = a_min / n, a_max / n
        b_min, b_max = b_min / self.bar_b_max, b_max / self.bar_b_max

        start, end = (a_max - a_min) * b_min + a_min, (a_max - a_min) * b_max + a_min

        return (start, end)

    def on_slider_change(self, value):
        # Check if audio file is even loaded
        if not self.audio_file:
            return

        a_min, a_max = self.time_selection_a.value()
        b_min, b_max = self.time_selection_b.value()

        if abs(a_max - a_min) < 10:
            return

        if abs(b_max - b_min) < 10:
            return
        
        start, end = self.read_range_bars()

        self.graph_view.set_audio(self.audio_file, start, end)
