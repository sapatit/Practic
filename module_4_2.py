def test_function():
    """
    Демонстрирует использование вложенной функции.
    """

    def inner_function():
        """
        Печатает сообщение, указывающее, что она находится в области видимости test_function.
        """
        print("Я в области видимости функции test_function")

    # Вызываем inner_function() внутри test_function()
    inner_function()


# Вызываем test_function()
test_function()

# Проверяем, существует ли inner_function() в локальной области видимости
if 'inner_function' in locals():
    # Пытаемся вызвать inner_function() вне test_function()
    inner_function()
else:
    print("Ошибка: inner_function не определена вне функции test_function")
