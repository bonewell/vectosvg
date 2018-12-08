#!/usr/bin/env python3
from abc import ABC, abstractmethod


class InterpreterInterface(ABC):
    @abstractmethod
    def interpret(self):
        pass


class IteratorInterface(ABC):
    @abstractmethod
    def next(self):
        pass
