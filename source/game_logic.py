from typing import Callable

class Trigger:
    def __init__(self):
        self.subscribers : list[Callable] = list()

    def subscribe(self, subscriber : Callable):
        self.subscribers.append(subscriber)

    def invoke(self, arg = ...):
        for subscriber in self.subscribers:
            subscriber(arg)