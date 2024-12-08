import pytest
from typing import Sequence
from functools import partial
from fractions import Fraction

from apply_functions_to_numbers import apply_all_func, FunctionResult, is_non_empty_sequence_of_numbers, \
    get_function_name, handle_function_result


def test_apply_all_func_with_valid_input():
    num_list = [1, 2, 3, 4, 5]
    functions = [max, min, sum, sorted]
    results = apply_all_func(num_list, *functions)
    assert len(results) == len(functions)
    for result in results:
        assert isinstance(result, FunctionResult)
        assert result.name in [get_function_name(f) for f in functions]
        assert result.result is not None


def test_apply_all_func_with_empty_input():
    with pytest.raises(TypeError):
        apply_all_func([])


def test_apply_all_func_with_non_number_input():
    with pytest.raises(TypeError):
        apply_all_func(["a", "b", "c"])


def test_apply_all_func_with_mixed_number_types():
    with pytest.raises(TypeError):
        apply_all_func([1, 2.0, 3, 4.0])


def test_apply_all_func_with_no_functions():
    with pytest.raises(ValueError):
        apply_all_func([1, 2, 3])


def test_apply_all_func_with_ignore_errors():
    num_list = [1, 2, 3]
    results = apply_all_func(num_list, lambda x: 1 / 0, ignore_errors=True)
    assert len(results) == 1
    assert "Error:" in results[0].result


def test_apply_all_func_with_none_function():
    num_list = [1, 2, 3]
    with pytest.raises(TypeError):
        apply_all_func(num_list, None)


def test_apply_all_func_with_non_callable():
    num_list = [1, 2, 3]
    with pytest.raises(TypeError):
        apply_all_func(num_list, 42)


def test_apply_all_func_with_function_requiring_more_args():
    def add(x, y):
        return x + y

    num_list = [1, 2, 3]
    with pytest.raises(TypeError):
        apply_all_func(num_list, add)


def test_apply_all_func_with_large_input():
    num_list = list(range(1000000))  # 1 million numbers
    functions = [max, min, sum]
    results = apply_all_func(num_list, *functions)
    assert len(results) == len(functions)


def test_get_function_name():
    def my_function(x):
        return x * 2

    assert get_function_name(my_function) == "my_function"
    assert get_function_name(partial(my_function, y=2)) == "partial(my_function, args=(), kwargs={'y': 2})"


def test_apply_all_func_with_function_returning_none():
    def return_none(x: Sequence[int]) -> None:
        return None

    num_list = [1, 2, 3]
    results = apply_all_func(num_list, return_none)
    assert len(results) == 1
    assert results[0].result is None


def test_handle_function_result_with_exception():
    result = handle_function_result(lambda x: x, Exception("Test error"), ignore_errors=True)
    assert result.result == "Error: Test error"
    assert result.name == "<lambda>"


def test_apply_all_func_with_decimal_numbers():
    from decimal import Decimal
    num_list = [Decimal('1.1'), Decimal('2.2'), Decimal('3.3')]
    functions = [sum, max]
    results = apply_all_func(num_list, *functions)
    assert len(results) == len(functions)
    assert results[0].result == Decimal('6.6')
    assert results[1].result == Decimal('3.3')


def test_apply_all_func_with_fraction_numbers():
    num_list = [Fraction(1, 2), Fraction(2, 3), Fraction(3, 4)]
    functions = [lambda x: sum(x, Fraction(0)), max]
    results = apply_all_func(num_list, *functions)
    assert len(results) == len(functions)
    assert results[1].result == Fraction(3, 4)  # max


def test_apply_all_func_with_ignore_errors_and_no_functions():
    num_list = [1, 2, 3]
    results = apply_all_func(num_list, ignore_errors=True)
    assert len(results) == 0


def test_apply_all_func_with_function_that_raises_error():
    def raise_error(x):
        raise ValueError("This is an error")

    num_list = [1, 2, 3]
    results = apply_all_func(num_list, raise_error, ignore_errors=True)
    assert len(results) == 1
    assert results[0].result.startswith("Error:")  # Check if error is handled


if __name__ == "__main__":
    pytest.main()
