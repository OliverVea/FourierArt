from collections import deque as Queue

class Choice:
    def __init__(self, choices: dict, history_length: int = 3):
        self.set_choices(choices)

        self.choice_key = self.keys[0]
        self.choice_val = self.vals[0]
        self.history_length = history_length
        self.history = Queue(maxlen=history_length)

    def set_choices(self, choices: dict):
        self.choices = choices
        self.keys = list(choices.keys())
        self.vals = list(choices.values())

    def get(self, return_key: bool = False, return_value: bool = True):
        if return_key and return_value:
            return (self.choice_key, self.choice_val)

        if return_key:
            return self.choice_key

        if return_value:
            return self.choice_val

    def set(self, key: str):
        if key in self.keys:
            self.history.append((self.choice_key, self.choice_val))
            self.choice_key = key
            self.choice_val = self.choices[key]

        else:
            raise Exception(f'Key value \'{key}\' invalid. Possible values are: {", ".join(self.keys)}.')