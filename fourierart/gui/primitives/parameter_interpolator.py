import numpy as np

class ParameterInterpolator():
    lin = lambda _, v: v
    exp = lambda self, v: (np.power(self.interpolator_order, v) - 1) / (self.interpolator_order - 1)
    log = lambda self, v: np.log(v * (self.interpolator_order - 1) + 1) / np.log(self.interpolator_order)

    def __init__(self, parameter, interpolator: str = 'lin', interpolator_order: int = 50):
        self.p = parameter
        self.interpolator = interpolator
        self.interpolator_order = interpolator_order

        interpolators = {'lin': (self.lin, self.lin), 'exp': (self.exp, self.log), 'log': (self.log, self.exp)}
        self.forward, self.backward = interpolators[interpolator]

    def slider_max(self):
        return (self.p.max - self.p.min) / self.p.step

    def from_slider(self, v: float):
        v = self.forward(v / self.slider_max())
        return  v * (self.p.max - self.p.min) + self.p.min

    def to_slider(self, v: float):
        v = self.backward((v - self.p.min) / (self.p.max - self.p.min))
        v = np.clip(v, 0, 1)

        return v * self.slider_max()
