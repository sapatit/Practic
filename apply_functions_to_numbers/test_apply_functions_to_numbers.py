import unittest
from unittest.mock import patch
from typing import Sequence, Union
from numbers import Number
from functools import partial
from apply_functions_to_numbers import (
    is_non_empty_sequence_of_numbers,
    get_function_name,
    handle_function_result,
    apply_all_func,
)


class TestFunctions(unittest.TestCase):
    def test_is_non_empty_sequence_of_numbers(self):
        self.assertTrue(is_non_empty_sequence_of_numbers([1, 2.0, 3]))
        self.assertFalse(is_non_empty_sequence_of_numbers([1, 2.0, "3"]))
        self.assertFalse(is_non_empty_sequence_of_numbers([]))

    def test_get_function_name(self):
        def example_function(x, y):
            return x + y

        self.assertEqual(get_function_name(example_function), "example_function")
        self.assertEqual(get_function_name(partial(example_function, y=2)),
                         "partial(example_function, args=(), kwargs={'y': 2})")

    def test_handle_function_result(self):
        def example_function(x: Sequence[Number]) -> int:
            return sum(x)

        result = handle_function_result(example_function, 15, ignore_errors=False)
        self.assertEqual(result.name, "example_function")
        self.assertEqual(result.result, 15)

        with patch("apply_functions_to_numbers.logging.error") as mock_error:
            result = handle_function_result(example_function, ValueError("Test error"), ignore_errors=True)
            mock_error.assert_called_with("Function example_function raised an error: Test error")
            self.assertEqual(result.name, "example_function")
            self.assertEqual(result.result, "Error: Test error")

    def test_apply_all_func(self):
        def example_function(x: Sequence[Number]) -> int:
            return sum(x)

        def example_function_error(x: Sequence[Number]) -> int:
            raise ValueError("Test error")

        # Test with valid input
        results = apply_all_func([1, 2, 3, 4], example_function, ignore_errors=False)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "example_function")
        self.assertEqual(results[0].result, 10)

        # Test with ignore_errors=True
        results = apply_all_func([1, 2, 3, 4], example_function, example_function_error, ignore_errors=True)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].name, "example_function")
        self.assertEqual(results[0].result, 10)
        self.assertEqual(results[1].name, "example_function_error")
        self.assertEqual(results[1].result, "Error: Test error")

        # Test with invalid input
        with self.assertRaises(TypeError):
            apply_all_func([1, 2, "3", 4], example_function)

        with self.assertRaises(ValueError):
            apply_all_func([1, 2, 3, 4])

    def test_apply_all_func_overload(self):
        def example_function_int(x: Sequence[int]) -> int:
            return sum(x)

        def example_function_float(x: Sequence[float]) -> float:
            return sum(x)

        # Test with int sequence
        results = apply_all_func([1, 2, 3, 4], example_function_int, ignore_errors=False)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "example_function_int")
        self.assertEqual(results[0].result, 10)

        # Test with float sequence
        results = apply_all_func([1.0, 2.0, 3.0, 4.0], example_function_float, ignore_errors=False)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "example_function_float")
        self.assertEqual(results[0].result, 10.0)

        # Test with mixed sequence (should raise TypeError)
        with self.assertRaises(TypeError):
            apply_all_func([1, 2.0, 3, 4.0], example_function_int, example_function_float)

    def test_is_non_empty_sequence_of_numbers_with_other_types(self):
        self.assertTrue(is_non_empty_sequence_of_numbers((1, 2.0, 3)))
        self.assertTrue(is_non_empty_sequence_of_numbers({1, 2.0, 3}))
        self.assertFalse(is_non_empty_sequence_of_numbers([1, 2.0, "3"]))

    def test_get_function_name_with_lambda(self):
        example_lambda = lambda x, y: x + y
        self.assertEqual(get_function_name(example_lambda), "<lambda>")

    def test_get_function_name_with_class_method(self):
        class ExampleClass:
            def example_method(self, x, y):
                return x + y

        self.assertEqual(get_function_name(ExampleClass.example_method), "example_method")

    def test_handle_function_result_with_other_errors(self):
        def example_function(x: Sequence[Number]) -> int:
            raise TypeError("Test error")

        with patch("apply_functions_to_numbers.logging.error") as mock_error:
            result = handle_function_result(example_function, TypeError("Test error"), ignore_errors=True)
            mock_error.assert_called_with("Function example_function raised an error: Test error")
            self.assertEqual(result.name, "example_function")
            self.assertEqual(result.result, "Error: Test error")

    def test_handle_function_result_with_none_output(self):
        def example_function(x: Sequence[Number]) -> int:
            return None

    def test_apply_all_func_with_empty_sequence(self):
        def example_function(x: Sequence[Number]) -> int:
            return sum(x)

        with self.assertRaises(TypeError):
            apply_all_func([], example_function, ignore_errors=False)

    def test_apply_all_func_with_sequence_containing_none(self):
        def example_function(x: Sequence[Number]) -> int:
            return sum(i for i in x if i is not None)  # Игнорируем None

        results = apply_all_func([1, 2, None, 4], example_function, ignore_errors=True)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "example_function")
        self.assertEqual(results[0].result, 7)

    def test_apply_all_func_overload_with_mixed_sequence(self):
        def example_function_int(x: Sequence[int]) -> int:
            return sum(x)

        def example_function_float(x: Sequence[float]) -> float:
            return sum(x)

        with self.assertRaises(TypeError):
            apply_all_func([1, 2.0, 3, 4.0], example_function_int, example_function_float)

    def test_apply_all_func_with_various_data_types(self):
        def example_function(x: Sequence[Number]) -> int:
            return sum(x)

        # Test with a list of integers
        results = apply_all_func([1, 2, 3], example_function, ignore_errors=False)
        self.assertEqual(results[0].result, 6)

        # Test with a tuple of floats
        results = apply_all_func((1.0, 2.0, 3.0), example_function, ignore_errors=False)
        self.assertEqual(results[0].result, 6.0)

        # Test with a set of mixed types (should raise TypeError)
        with self.assertRaises(TypeError):
            apply_all_func({1, 2, "3"}, example_function)

    def test_handle_function_result_with_empty_input(self):
        def example_function(x: Sequence[Number]) -> int:
            if not x:  # Проверка на пустой список
                return 0
            return sum(x)

        result = handle_function_result(example_function, example_function([]), ignore_errors=False)
        self.assertEqual(result.name, "example_function")
        self.assertEqual(result.result, 0)

    def test_apply_all_func_with_none_in_sequence(self):
        def example_function(x: Sequence[Number]) -> int:
            return sum(i for i in x if i is not None)

        results = apply_all_func([1, 2, None, 4], example_function, ignore_errors=True)
        self.assertEqual(results[0].result, 7)


if __name__ == "__main__":
    unittest.main()
