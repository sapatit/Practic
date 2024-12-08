## Назначение программы

Данная программа предоставляет функциональность для применения нескольких функций к списку чисел. Она позволяет обрабатывать результаты выполнения функций, включая обработку ошибок, и возвращает результаты в удобном формате. Программа поддерживает работу с последовательностями чисел (целых и дробных) и может использоваться для различных математических операций, таких как нахождение максимума, минимума, суммы и сортировки.

## Использование

### Импорт функций

Для использования функций из модуля `apply_functions_to_numbers`, импортируйте их в вашем Python-скрипте:

```python
from apply_functions_to_numbers import apply_all_func, FunctionResult
```

### Пример использования

Вот пример, демонстрирующий основные функции программы:

```python
from apply_functions_to_numbers import apply_all_func

def example_usage():
    # Применяем функции к списку чисел
    results = apply_all_func([6, 20, 15, 9], max, min, sum, sorted)

    for res in results:
        print(f"{res.name}: {res.result}")

if __name__ == "__main__":
    example_usage()
```

### Описание функций

- `apply_all_func(num_list: Sequence[Union[int, float]], *functions: Callable, ignore_errors: bool = False) -> List[FunctionResult]`: Применяет указанные функции к списку чисел и возвращает список объектов `FunctionResult`, содержащих имя функции, результат и метаданные.

- `is_non_empty_sequence_of_numbers(seq: Sequence[Number]) -> bool`: Проверяет, является ли последовательность непустой и содержит ли только числа.

- `get_function_name(func: Callable) -> str`: Получает имя функции, учитывая возможность использования `functools.partial`.

- `handle_function_result(func: Callable, result: Any, ignore_errors: bool) -> FunctionResult`: Обрабатывает результат выполнения функции и возвращает объект `FunctionResult`.

### Примеры функций

```python
def multiply(x: int, y: int) -> int:
    """Умножает два числа."""
    return x * y

# Применяем функции к списку чисел
results = apply_all_func([1, 2, 3, 4], max, min, sum, sorted)

for res in results:
    print(f"{res.name}: {res.result}")
```

## Тестирование

Программа включает тесты, написанные с использованием `unittest` и `pytest`. Вы можете запустить тесты, чтобы убедиться, что все функции работают корректно.

### Запуск тестов

Для запуска тестов с использованием `unittest`, выполните следующую команду:

```bash
python -m unittest test_apply_functions_to_numbers.py
```

Для запуска тестов с использованием `pytest`, выполните:

```bash
pytest pytest_apply_functions_to_numbers.py
```

## Заключение

Программа предоставляет удобный интерфейс для применения функций к числовым последовательностям, что делает её полезным инструментом для разработчиков, работающих с данными и математическими операциями.