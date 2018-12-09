#!/usr/bin/env python3
from abc import ABC, abstractmethod
from command.command import Command


class Iterator(object):
    def __init__(self, c):
        self._c = c

    def __iter__(self):
        return self

    def __next__(self):
        cmd = self._c.next()
        if cmd:
            return cmd
        else:
            raise StopIteration()


class InterpreterInterface(ABC):
    @abstractmethod
    def next(self) -> Command or None:
        pass

    def __iter__(self):
        return Iterator(self)
