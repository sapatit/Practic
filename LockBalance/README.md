# Bank Operations Simulation

## Описание

Данная программа реализует симуляцию банковских операций с использованием многопоточности в Python. Она позволяет выполнять операции пополнения и снятия средств с баланса банка, обеспечивая корректное управление потоками с помощью блокировок.

### Основные функции

- **Пополнение баланса**: Метод `deposit` выполняет 100 транзакций пополнения, увеличивая баланс на случайное целое число от 50 до 500.
- **Снятие средств**: Метод `take` выполняет 100 транзакций снятия. Если запрашиваемая сумма меньше или равна текущему балансу, она снимается. В противном случае выводится сообщение о недостатке средств.
- **Потокобезопасность**: Используются объекты класса `Lock` для предотвращения состояния гонки при одновременных операциях пополнения и снятия.

## Использование

Запустите программу, чтобы увидеть симуляцию банковских операций:

```bash
python scripts.py
```

## Тестирование

Для проверки функциональности программы используются юнит-тесты, написанные с использованием модуля `unittest`. Чтобы запустить тесты, выполните следующую команду:

```bash
python -m unittest test_scripts.py
```

### Описание тестов

- **test_initial_balance**: Проверяет, что начальный баланс равен 0.
- **test_deposit**: Проверяет, что метод `deposit` корректно увеличивает баланс.
- **test_take**: Проверяет, что метод `take` корректно уменьшает баланс.
- **test_take_insufficient_funds**: Проверяет, что метод `take` не позволяет снимать больше, чем есть на счете.
- **test_concurrent_deposit_and_take**: Проверяет, что одновременные операции `deposit` и `take` работают корректно и баланс не становится отрицательным.

## Лицензия

Этот проект лицензирован под MIT License - смотрите файл [LICENSE](LICENSE) для подробностей.