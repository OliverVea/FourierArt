class Callback():
    def __init__(self, callbacks: set = None):
        self.callbacks = callbacks if callbacks else set()

    def register(self, callback):
        self.callbacks.add(callback)

    def unregister(self, callback):
        self.callbacks.remove(callback)
    
    def __call__(self):
        self.callback()

    def callback(self):
        for callback in self.callbacks:
            callback()

class ArgumentCallback(Callback):
    def callback(self, value):
        for callback in self.callbacks:
            callback(value)