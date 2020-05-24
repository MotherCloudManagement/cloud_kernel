import random
import inspect


def generate_secret(length=128):
    chars = "0123456789"\
        "abcdefghijklmnopqrstuvwxyz"\
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"\
        ".,_-+*@:;[](){}~!?|<>=/\&$#"
    return "".join(random.choice(chars) for _ in range(length))


class EventRegister(object):

    def __init__(self):
        self.listeners = []

    def __iter__(self):
        for listener in self.listeners:
            yield listener

    def listen(self, listener):

        assert inspect.isroutine(listener), "Invalid Listener"
        if listener not in self.listeners:
            self.listeners.append(listener)

        return listener
