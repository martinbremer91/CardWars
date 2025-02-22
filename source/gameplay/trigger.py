class Trigger:
    def __init__(self, trigger_type):
        self.subscribers = list()
        self.trigger_type = trigger_type

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)
    def unsubscribe(self, subscriber):
        if subscriber in self.subscribers:
            self.subscribers.remove(subscriber)
        else:
            raise Exception(f'Failed to unsubscribe effect {subscriber}: not in {self} subscriber list')

    def invoke(self):
        for subscriber in self.subscribers:
            subscriber()