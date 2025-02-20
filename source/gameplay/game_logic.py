from typing import Callable

class Trigger:
    def __init__(self):
        self.subscribers : list[Callable] = list()

    def subscribe(self, subscriber : Callable):
        self.subscribers.append(subscriber)

    def invoke(self, arg = ...):
        for subscriber in self.subscribers:
            subscriber(arg)

class Choice[T]:
    def __init__(self, options : list[T]):
        self.options : list[T] = options
        self.type_label : str = f"{type(options[0]).__name__}"

    def resolve(self) -> T:
        while True:
            user_prompt_options: str = ''
            for i in range(len(self.options)):
                user_prompt_options += f'[{i}]: {self.options[i]}\n'

            print(f'Available {self.type_label}s:\n{user_prompt_options}')
            index = input(f'Select {self.type_label}:')

            if not index.isdigit():
                print(f'invalid {self.type_label} index: not a digit')
                continue
            index = int(index)
            if index < 0 or index >= len(self.options):
                print(f'invalid {self.type_label} index: digit out of range')
                continue

            return self.options[index]