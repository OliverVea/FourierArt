from fourierart.gui.primitives.parameter import Parameter

class Range(Parameter):
    def set(self, value: tuple):
        for i, v in enumerate(value):
            if self.hard_min:
                value[i] = max(v, self.min)

            if self.hard_max:
                value[i] = min(v, self.max)
                
        self.value = value