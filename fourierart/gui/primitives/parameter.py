import numpy as np

class Parameter:
    def __init__(self, min: float, max: float, value, step: float, hard_min: bool = True, hard_max: bool = False, format: str = lambda v: f'{v}', dtype = float):
        self.min = min
        self.max = max
        self.value = value
        self.step = step
        self.hard_min = hard_min
        self.hard_max = hard_max
        self.format = format
        self.dtype = dtype

    def get(self):
        return self.value

    def set(self, value: float):
        min = self.min if self.hard_min else None
        max = self.max if self.hard_max else None

        self.value = np.clip(value, min, max)

        self.value = self.dtype(self.value)

        return self.value