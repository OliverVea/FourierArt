import numpy as np

class Parameter:
    def __init__(self, min, max, value, step, hard_min: bool = True, hard_max: bool = False, format = lambda v: f'{v}'):
        self.min = min
        self.max = max
        self.value = value
        self.step = step
        self.hard_min = hard_min
        self.hard_max = hard_max
        self.format = format

    def get(self):
        return self.value

    def set(self, value):
        if self.hard_min:
            value = max(value, self.min)

        if self.hard_max:
            value = min(value, self.max)

        self.value = value

class Range(Parameter):
    def set(self, value):
        for i, v in enumerate(value):
            if self.hard_min:
                value[i] = max(v, self.min)

            if self.hard_max:
                value[i] = min(v, self.max)
                
        self.value = value

class ParameterInterpolator():
    lin = lambda _, v: v
    exp = lambda self, v: (np.power(self.k, v) - 1) / (self.k - 1)
    log = lambda self, v: np.log(v * (self.k - 1) + 1) / np.log(self.k)

    def __init__(self, parameter, interpolator, interpolator_order):
        self.p = parameter
        self.interpolator = interpolator
        self.k = interpolator_order

        interpolators = {'lin': (self.lin, self.lin), 'exp': (self.exp, self.log), 'log': (self.log, self.exp)}
        self.forward, self.backward = interpolators[interpolator]

    def from_slider(self, v):
        v = self.forward(v / self.slider_max())
        return  v * (self.p.max - self.p.min) + self.p.min

    def to_slider(self, v):
        v = self.backward((v - self.p.min) / (self.p.max - self.p.min))
        v = np.clip(v, 0, 1)

        return v * self.slider_max()

    def slider_max(self):
        return (self.p.max - self.p.min) / self.p.step