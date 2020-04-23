from functools import partial, wraps
from inspect import signature
from typing import Callable
from collections.abc import Iterable


class _pipe:

    def __init__(self, fnc: Callable):
        self.fnc = fnc
        self.inpt = None
        self.arity = len(dict(signature(fnc).parameters))
        self.args = None

    def run(self):
        if not self.inpt:
            if not self.args:
                return self.fnc()
            return self.fnc(*self.args)

        args = self.inpt.run()
        
        if isinstance(args, Iterable):
            return self.fnc(*args)
        return self.fnc(args)

    def __call__(self, *args):
        self.args = args
        return self

    def __or__(self, other):
        if not other.arity:
            raise ValueError("The righthand expression must be of arity >= 1")
        
        other.inpt = self
        return other


def pipe(fnc):
    @wraps(fnc)
    def wrapper(*args):
        return fnc(*args)
    return _pipe(wrapper)
