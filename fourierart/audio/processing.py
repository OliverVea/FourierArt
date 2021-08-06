import numpy as np
import matplotlib.pyplot as plt
from pydub.audio_segment import AudioSegment

from scipy.signal import butter, sosfiltfilt, sosfreqz
from scipy.signal.signaltools import resample

class WindowFunction:
    Blackman = 1
    Hanning = 1

    @staticmethod
    def get_window_function(window_function):
        if window_function == WindowFunction.Blackman:
            return np.blackman

        if window_function == WindowFunction.Hanning:
            return np.hanning

    @staticmethod
    def apply_window(data, window_function):
        window_function = WindowFunction.get_window_function(window_function)
        window = window_function(len(data))

        return np.multiply(data, window)

    @staticmethod
    def plot_window(data, window_function, show=False):
        window_function = WindowFunction.get_window_function(window_function)
        window = window_function(len(data))

        windowed_data = np.multiply(data, window)

        fig, axs = plt.subplots(3, 1)

        axs[0].set_title('Raw Data')
        axs[0].plot(data)

        axs[1].set_title('Window')
        axs[1].plot(window)

        axs[2].set_title('Windowed Data')
        axs[2].plot(windowed_data)

        plt.tight_layout()

        if show:
            plt.show()

class Filter:
    @staticmethod
    def butterworth(data, order: int, critical_freq, sample_rate: float, filter_type: str = 'lowpass'):
        sos = butter(order, critical_freq, filter_type, fs=sample_rate, output='sos')
        data = sosfiltfilt(sos, data)

        return data

    @staticmethod
    def plot_butterworth(order: int, critical_freq, sample_rate: float, filter_type: str = 'lowpass', show: bool = False):
        sos = butter(order, critical_freq, filter_type, fs=sample_rate, output='sos')

        w, h = sosfreqz(sos)
        db = 20*np.log10(np.maximum(np.abs(h), 1e-5))
        plt.plot(w/np.pi*sample_rate/2, db)

        if show:
            plt.show()


def get_spectrogram(audio, window_width, window_function: int = None, step_size: int = 1, use_zero_padding: bool = True, normalize_amplitudes: bool = False):
    # Initialize empty spectogram. 
    # This will be filled with lists containing frequency amplitudes.
    spectrogram = []

    # Calculate FFT steps in the spectrogram
    if use_zero_padding:
        n_steps = len(audio) // step_size + 1

    else:
        n_steps = (len(audio) - window_width) // step_size + 1

    for i_step in range(n_steps):
        if use_zero_padding:
            start = step_size * i_step - window_width // 2
            start = max(0, start)

            end = start + window_width // 2
            end = min(end, len(audio))

        # Extract audio sample
        audio_sample = audio[start:end]

        # Apply window function if used
        if window_function:
            audio_sample = WindowFunction.apply_window(audio_sample, window_function)

        # Do FFT
        fft_result = np.fft.rfft(audio_sample, n=window_width)

        # Frequency amplitude calculation
        bin_amplitudes = np.abs(fft_result)

        # Amplitude normalization
        if normalize_amplitudes:
            bin_amplitudes /= np.sum(bin_amplitudes) 

        spectrogram.append(bin_amplitudes)

    # Calculate axis values
    y = np.array([i for i in range(window_width // 2 + 1)])
    x = np.array([i * step_size for i in range(n_steps)])

    return np.array(spectrogram), x, y

def downsample(audio_segment: AudioSegment, num, method: str = 'set_frame_rate', resample_threshold: int = 1e5):
    arr = np.array(audio_segment.get_array_of_samples())

    if len(arr) > resample_threshold:
        indeces = np.linspace(0, len(arr) - 1, num, dtype=np.int32)
        return arr[indeces]

    downsample_factor = num / len(arr)

    if method == 'set_frame_rate':
        fs = audio_segment.frame_rate
        audio = audio_segment.set_frame_rate(int(fs * downsample_factor))
        return np.array(audio.get_array_of_samples())

    if method == 'resample':
        return resample(arr, num)

    raise Exception(f'method "{method}" not understood. please use one of the implemented methods. (\'set_frame_rate\' or \'resample\')')