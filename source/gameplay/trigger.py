class Trigger:
    def __init__(self):
        self.subscribers = list()
        self.invoking = False
        self.subscribe_queue = list()
        self.unsubscribe_queue = list()

    def subscribe(self, subscriber):
        if self.invoking:
            self.subscribe_queue.append(subscriber)
            return
        self.internal_subscribe(subscriber)
    def internal_subscribe(self, subscriber):
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
        if self.subscribe_queue:
            for subscriber in self.subscribe_queue:
                self.internal_subscribe(subscriber)
        self.invoking = False