from functools import wraps
from inspect import signature, Signature
from typing import Any, Callable, Union
from collections.abc import Iterable


def _get_signature(fnc: Callable) -> Signature:
    return signature(fnc)


def _get_ret_type(fnc: Callable) -> type:
    sig = _get_signature(fnc)
    ret_type = sig.return_annotation
    return ret_type


def _get_arg_type(fnc: Callable) -> type:
    sig = _get_signature(fnc)
    params = list(sig.parameters.values())
    arg_type = params[0].annotation
    return arg_type


def check_types(fnc1: Callable, fnc2: Callable) -> bool:
    fnc1_ret = _get_ret_type(fnc1)
    fnc2_arg = _get_arg_type(fnc2)
    return fnc1_ret == fnc2_arg


class _pipe:

    def __init__(self, fnc: Callable):
        self.fnc: Callable = fnc
        self.inpt: Union[None, _pipe] = None
        self.arity: int = len(dict(_get_signature(fnc).parameters))
        self.args: Union[None, Any] = None

    def run(self) -> Any:
        if not self.inpt:
            if not self.args:
                return self.fnc()
            return self.fnc(*self.args)

        args = self.inpt.run()

        if isinstance(args, Iterable):
            return self.fnc(*args)
        return self.fnc(args)

    def __call__(self, *args: Any):
        self.args = args
        return self

    def __or__(self, other):
        if not other.arity:
            raise ValueError("The righthand expression must be of arity >= 1")

        if not check_types(self.fnc, other.fnc):
            raise TypeError("The function signatures do not match")
        
        other.inpt = self
        return other


def pipe(fnc: Callable):
    @wraps(fnc)
    def wrapper(*args: Any):
        return fnc(*args)
    return _pipe(wrapper)
