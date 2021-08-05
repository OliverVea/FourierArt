from queue import Queue

class Choice:
    def __init__(self, choices: dict, history_length: int = 3):
        self.set_choices(choices)

        self.choice_key = self.keys[0]
        self.choice_val = self.vals[0]
        self.history_length = history_length
        self.history = Queue(history_length)

    def set_choices(self, choices: dict):
        self.choices = choices
        self.keys = list(choices.keys())
        self.vals = list(choices.values())

    def get(self):
        pass

    def set(self, key: str):
        if key in self.keys:
            self.history.put((self.key, self.val))
            self.choice_key = key
            self.choice_val = self.choices[key]

        else:
            raise Exception(f'Key value \'{key}\' invalid. Possible values are: {", ".join(self.keys)}.')