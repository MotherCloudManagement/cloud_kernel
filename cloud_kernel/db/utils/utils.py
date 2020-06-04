import random
import inspect
from sqlalchemy.orm import class_mapper, object_mapper


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


def retrieve_private_key(sa_variant):
    """ Return the Private Key name of a given object/class \'sa_variant\' """
    mapper = class_mapper(sa_variant) if inspect.isclass(sa_variant) \
        else object_mapper(sa_variant)

    return mapper.primary_key[0].key


