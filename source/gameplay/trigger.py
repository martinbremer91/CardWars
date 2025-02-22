class Trigger:
    def __init__(self, trigger_type):
        self.subscribers = list()
        self.trigger_type = trigger_type

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def invoke(self):
        for subscriber in self.subscribers:
            subscriber()