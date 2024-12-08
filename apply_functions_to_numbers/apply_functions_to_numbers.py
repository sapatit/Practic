from typing import List, Callable, Sequence, Union, Any, overload, Protocol, TypeVar, Optional
from dataclasses import dataclass, field
from numbers import Number
import logging
from functools import partial

# Настройка логирования
logging.basicConfig(level=logging.INFO)


# Определяем протокол для функций
class FunctionProtocol(Protocol):
    def __call__(self, num_list: Sequence[Number]) -> Any:
        ...


# Обобщенный тип
T = TypeVar('T', int, float, str, list, dict, Any)


@dataclass
class FunctionResult:
    name: str
    result: Optional[Any] = field(default=None)
    metadata: str = field(default="")


def is_non_empty_sequence_of_numbers(seq: Sequence[Number]) -> bool:
    """Проверяет, является ли последовательность непустой и содержит ли только числа (игнорируя None)."""
    return len(seq) > 0 and all(isinstance(i, Number) for i in seq if i is not None)


def get_function_name(func: Callable) -> str:
    """Получает имя функции, учитывая возможность использования functools.partial."""
    if hasattr(func, 'func'):
        original_func_name = getattr(func.func, '__name__', str(func.func))
        args = func.args
        kwargs = func.keywords
        return f"partial({original_func_name}, args={args}, kwargs={kwargs})"
    return getattr(func, '__name__', str(func))


def handle_function_result(func: Callable, result: Any, ignore_errors: bool) -> FunctionResult:
    """Обрабатывает результат выполнения функции и возвращает объект FunctionResult."""
    func_name = get_function_name(func)
    if isinstance(result, Exception) and ignore_errors:
        logging.error(f"Function {func_name} raised an error: {result}")
        return FunctionResult(name=func_name, result=f"Error: {str(result)}")
    else:
        logging.info(f"Function {func_name} applied successfully with result: {result}")
        return FunctionResult(name=func_name, result=result)


@overload
def apply_all_func(num_list: Sequence[int], *functions: Callable[[Sequence[int]], Any], ignore_errors: bool = False) -> \
List[FunctionResult]: ...


@overload
def apply_all_func(num_list: Sequence[float], *functions: Callable[[Sequence[float]], Any],
                   ignore_errors: bool = False) -> List[FunctionResult]: ...


def apply_all_func(num_list: Sequence[Union[int, float]], *functions: FunctionProtocol, ignore_errors: bool = False) -> \
List[FunctionResult]:
    if not is_non_empty_sequence_of_numbers(num_list):
        raise TypeError("num_list must be a non-empty sequence of numbers (int or float).")

    # Проверка на смешанные типы
    if any(isinstance(x, float) for x in num_list) and any(isinstance(x, int) for x in num_list):
        raise TypeError("num_list must contain only int or only float, not both.")

    if not functions:
        if ignore_errors:
            return []
        else:
            raise ValueError("At least one callable function must be provided.")

    results = []
    for func in functions:
        try:
            result = func(num_list)
            results.append(handle_function_result(func, result, ignore_errors))
        except Exception as e:
            if ignore_errors:
                results.append(handle_function_result(func, e, ignore_errors))
            else:
                raise
    return results


def example_usage():
    def multiply(x: T, y: T) -> T:
        """Умножает два числа."""
        return x * y

    # Создаем частичную функцию, которая умножает на 2
    partial_multiply = partial(multiply, y=2)

    # Применяем функции к списку чисел
    results = apply_all_func([6, 20, 15, 9], max, min, sum, sorted, lambda nums: [partial_multiply(n) for n in nums],
                             ignore_errors=True)

    for res in results:
        print(f"{res.name}: {res.result}")


if __name__ == "__main__":
    example_usage()
