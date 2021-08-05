from typing import Callable
from pydub import AudioSegment
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Colormap
from matplotlib import cm

from fourierart.audio_processing import WindowFunction, get_spectrogram, Filter
from fourierart.utility import slice_array

from scipy.interpolate import CubicSpline
from scipy.signal import resample

class AudioFile:
    def __init__(self, path: str = None, audio_segment: AudioSegment = None):
        self.path = path

        if audio_segment:
            self.audio_segment = audio_segment

        elif path:
            self.audio_segment = AudioSegment.from_wav(path)

        else:
            raise Exception('AudioFile initialization should specify either path or a pre-loaded AudioSegment.')

        self.audio = np.array(self.audio_segment.get_array_of_samples())

        self.fs = self.audio_segment.frame_rate
        self.n = len(self.audio)
        self.t = self.audio_segment.duration_seconds
        self.sample_width = self.audio_segment.sample_width
        self.channels = self.audio_segment.channels

        self.zoom_levels = self.get_zoom_index(1) + 1

        # TODO: Make load screen
        self.audio = [ self.audio ] + [self.downsample(self.audio, int(self.n / pow(2, i + 1))) for i in range(self.zoom_levels - 1)]

    def __ne__(self, other):
        # TODO
        return True

    def __eq__(self, other):
        # TODO
        return False

    def downsample(self, arr, num, method: str = 'set_frame_rate'):
        if len(arr) > 1e5:
            indeces = np.linspace(0, len(arr) - 1, num, dtype=np.int32)
            return arr[indeces]

        downsample_factor = num / self.n

        if method == 'set_frame_rate':
            audio = self.audio_segment.set_frame_rate(int(self.fs * downsample_factor))
            return np.array(audio.get_array_of_samples())

        if method == 'resample':
            return resample(arr, num)

        raise Exception(f'method "{method}" not understood. please use one of the implemented methods. (\'set_frame_rate\' or \'resample\')')

    def get_zoom_index(self, zoom_level, min_px = 1500):
        return int(np.log2(zoom_level * self.n / min_px))

    def get_time_amplitudes(self, start: float = 0.0, end: float = 1.0, downsample_factor: float = 1.0, normalize=True, normalization='max', gain: float = 1.0):
        zoom_index = self.get_zoom_index(end - start)

        arr = self.audio[zoom_index]
        n = len(arr)

        st = int(n * start)
        en = int(n * end)
        
        t = [self.t / (n - 1) * i + self.t * start for i in range(en - st)]
        arr = arr[st:en]

        if normalize:
            if normalization == 'max':
                arr = np.divide(arr, self.audio_segment.max_possible_amplitude)

            if normalization == 'peak':
                arr = np.divide(arr, np.max(arr))

        arr = np.multiply(arr, gain)

        return t, arr

    def as_array(self, start: float = 0.0, end: float = 1.0, normalize=True, normalization='max'):
        arr = np.copy(self.audio[0])
        arr = slice_array(arr, start, end)

        if normalize:
            if normalization == 'max':
                arr = np.divide(arr, self.audio_segment.max_possible_amplitude)

            if normalization == 'peak':
                arr = np.divide(arr, np.max(arr))

        return arr
        