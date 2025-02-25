class Trigger:
    def __init__(self):
        self.subscribers = list()
        self.invoking = False
        self.unsubscribe_queue = list()

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)
    def unsubscribe(self, subscriber):
        if self.invoking:
            self.unsubscribe_queue.append(subscriber)
            return
        self.internal_unsubscribe(subscriber)
    def internal_unsubscribe(self, subscriber):
        if subscriber in self.subscribers:
            self.subscribers.remove(subscriber)
        else:
            raise Exception(f'Failed to unsubscribe effect {subscriber}: not in {self} subscriber list')

    def invoke(self):
        self.invoking = True
        for subscriber in self.subscribers:
            subscriber()

        if self.unsubscribe_queue:
            for subscriber in self.unsubscribe_queue:
                self.internal_unsubscribe(subscriber)
        self.invoking = False