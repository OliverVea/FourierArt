from fourierart.gui.primitives.parameter import Parameter

class Range(Parameter):
    def set(self, value: tuple):
        lower, upper = value

        lower = max(lower, self.min) if self.hard_min else lower
        upper = min(upper, self.max) if self.hard_max else upper
                
        self.value = (lower, upper)

        return self.value