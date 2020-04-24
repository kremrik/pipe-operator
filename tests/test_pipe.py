from pipe.pipe import _pipe, pipe, _get_arg_type, _get_ret_type, check_types
import unittest
from unittest import skip
from functools import partial
from typing import List, Tuple


class test_pipe(unittest.TestCase):

    def test_no_args_single_pipe(self):
        fnc = lambda: 1
        proc = _pipe(fnc)
        gold = 1
        output = proc().run()
        self.assertEqual(gold, output)

    def test_one_arg_single_pipe(self):
        fnc = lambda x: x + 1
        proc = _pipe(fnc)
        gold = 2
        output = proc(1).run()
        self.assertEqual(gold, output)

    def test_mult_args_single_pipe(self):
        fnc = lambda x, y: x * y
        proc = _pipe(fnc)
        gold = 6
        output = proc(2, 3).run()
        self.assertEqual(gold, output)
    
    def test_bad_other_arity(self):
        fnc1 = lambda x: x + 1
        fnc2 = lambda: 1
        proc1 = _pipe(fnc1)
        proc2 = _pipe(fnc2)
        with self.assertRaises(ValueError):
            proc1(1) | proc2

    def test_two_pipes(self):
        fnc1 = lambda x: x + 1
        fnc2 = lambda y: y + 1
        proc1 = _pipe(fnc1)
        proc2 = _pipe(fnc2)
        gold = 3
        output = proc1(1) | proc2
        output = output.run()
        self.assertEqual(gold, output)

    def test_mult_pipes(self):
        fnc1 = lambda: 1
        fnc2 = lambda y: y + 1
        fnc3 = lambda z: z + 1
        proc1 = _pipe(fnc1)
        proc2 = _pipe(fnc2)
        proc3 = _pipe(fnc3)
        gold = 3
        output = proc1 | proc2 | proc3
        output = output.run()
        self.assertEqual(gold, output)

    def test_useless_args(self):
        fnc1 = lambda x: x + 1
        fnc2 = lambda y: y + 1
        proc1 = _pipe(fnc1)
        proc2 = _pipe(fnc2)
        gold = 3
        output = proc1(1) | proc2(4)  # proc2 arg does nothing but set self.args
        output = output.run()
        self.assertEqual(gold, output)

    def test_second_pipe_mult_inputs(self):
        fnc1 = lambda: (2, 3)
        fnc2 = lambda x, y: x * y
        proc1 = _pipe(fnc1)
        proc2 = _pipe(fnc2)
        gold = 6
        output = proc1() | proc2
        output = output.run()
        self.assertEqual(gold, output)

    def test_first_pipe_no_call(self):
        fnc1 = lambda: (2, 3)
        fnc2 = lambda x, y: x * y
        proc1 = _pipe(fnc1)
        proc2 = _pipe(fnc2)
        gold = 6
        output = proc1 | proc2
        output = output.run()
        self.assertEqual(gold, output)

    def test_mismatched_fnc_signatures(self):
        @pipe
        def f1() -> int:
            return 1
        @pipe
        def f2(x: str) -> str:
            return x.strip()
        with self.assertRaises(TypeError):
            f1 | f2


class test_get_ret_type(unittest.TestCase):

    def test_one_return_type(self):
        def f1(x: int) -> int:
            return x + 1
        gold = int
        output = _get_ret_type(f1)
        self.assertEqual(gold, output)


class test_get_arg_type(unittest.TestCase):

    def test_one_arg_type(self):
        def f1(x: int) -> int:
            return x + 1
        gold = int
        output = _get_arg_type(f1)
        self.assertEqual(gold, output)


class test_check_types(unittest.TestCase):

    def test_ints(self):
        def f1(x: int) -> int:
            return x + 1
        def f2(y: int) -> int:
            return y * 2

        gold = True
        output = check_types(f1, f2)
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
