import pytest
from iterator_example import Iterator, StepValueError

def test_step_zero():
    """Тест на случай, когда шаг равен 0."""
    with pytest.raises(StepValueError):
        Iterator(0, 10, 0)

def test_positive_iteration():
    """Тест на положительную итерацию."""
    iter_obj = Iterator(0, 5, 1)
    result = list(iter_obj)
    assert result == [0, 1, 2, 3, 4, 5]

def test_negative_iteration():
    """Тест на отрицательную итерацию."""
    iter_obj = Iterator(5, 0, -1)
    result = list(iter_obj)
    assert result == [5, 4, 3, 2, 1, 0]

def test_reset():
    """Тест на сброс итератора."""
    iter_obj = Iterator(0, 5, 1)
    list(iter_obj)  # Проходим итерацию
    iter_obj.reset()  # Сбрасываем
    result = list(iter_obj)  # Проходим итерацию снова
    assert result == [0, 1, 2, 3, 4, 5]

def test_reverse_iteration():
    """Тест на итерацию в обратном направлении."""
    iter_obj = Iterator(10, 5, -1)
    result = list(iter_obj)
    assert result == [10, 9, 8, 7, 6, 5]

def test_empty_iteration():
    """Тест на случай, когда итерация не должна возвращать значения."""
    iter_obj = Iterator(5, 1, 1)
    result = list(iter_obj)
    assert result == []

if __name__ == "__main__":
    pytest.main()
