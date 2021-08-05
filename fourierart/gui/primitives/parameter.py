class Parameter:
    def __init__(self, min: float, max: float, value, step: float, hard_min: bool = True, hard_max: bool = False, format: str = lambda v: f'{v}'):
        self.min = min
        self.max = max
        self.value = value
        self.step = step
        self.hard_min = hard_min
        self.hard_max = hard_max
        self.format = format

    def get(self):
        return self.value

    def set(self, value: float):
        if self.hard_min:
            value = max(value, self.min)

        if self.hard_max:
            value = min(value, self.max)

        self.value = value