from pydub import AudioSegment
import numpy as np

from fourierart.audio.processing import downsample

class AudioFile:
    @staticmethod
    def from_file(path: str = None):
        audio_file = AudioFile(AudioSegment.from_wav(path))
        audio_file.path = path

        return audio_file

    def __init__(self, audio_segment: AudioSegment):
        self.path = None # Will (only) be set in the from_file method.
        self.audio_segment = audio_segment.set_channels(1) # TODO: This enforces mono audio.

        # Array contains samples from original mono track and then iteratively 2x more downscaled samples.
        self.audio = [np.array(self.audio_segment.get_array_of_samples())]

        # Initializing audio parameter shorthands
        self.fs = self.audio_segment.frame_rate
        self.n  = len(self.audio[0])
        self.t  = self.audio_segment.duration_seconds
        self.w  = self.audio_segment.sample_width
        self.c  = self.audio_segment.channels

        self.zoom_levels = self.get_zoom_index(1) + 1

        # TODO: Make load screen
        downsampled_sizes = [int(self.n / pow(2, i + 1)) for i in range(self.zoom_levels - 1)]
        self.audio += [downsample(self.audio_segment.set_channels(1), size) for size in downsampled_sizes]

    def __ne__(self, other):
        print('Bad __ne__ used in audio_file')
        # TODO
        return True

    def __eq__(self, other):
        print('Bad __eq__ used in audio_file')
        # TODO
        return False

    def get_zoom_index(self, zoom_level, min_px = 1500):
        return max(0, int(np.log2(zoom_level * self.n / min_px)))

    def get_amplitudes(self, 
        start: float = 0.0, 
        end: float = 1.0, 
        use_downscaling: bool = False, 
        return_time: bool = False, # If the function returns the time values corresponding to the amplitude values.
        normalize=True, 
        normalization='max', # Type of normalization. 'max' normalizes after the max value with the audio bit-depth, 'peak' normalizes after the highest sampled value.
        gain: float = 1.0,
        abs: bool = False,
        clip: bool = False, # If the output signal is limited between 0 and 1
    ):
        zoom_index = self.get_zoom_index(end - start) if use_downscaling else 0
        arr = self.audio[zoom_index]

        n = len(arr)

        start, end = int(n * start), int(n * end)
        arr = arr[start:end]

        if normalize:
            max = self.audio_segment.max_possible_amplitude if normalization == 'max' else np.max(arr)
            arr = np.divide(arr, max)

        if gain != 1.0:
            arr = np.multiply(arr, gain)

        if abs:
            arr = np.abs(arr)

        if clip:
            arr = np.clip(arr, 0, 1)

        if return_time:
            t = [self.t / (n - 1) * i + self.t * start for i in range(end - start)]
            return t, arr
        
        return arr
        