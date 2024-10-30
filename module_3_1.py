calls = 0

def count_calls():
    global calls
    calls += 1

def string_info(string):
    count_calls()
    length = len(string)
    upper_case = string.upper()
    lower_case = string.lower()
    return (length, upper_case, lower_case)

def is_contains(string, list_to_search):
    count_calls()
    string_lower = string.lower()
    for item in list_to_search:
        if string_lower in item.lower():
            return True
    return False

print(string_info('Capybara'))
print(string_info('Armageddon'))
print('Статус строки в этом списке:', is_contains('Urban', ['ban', 'BaNaN', 'urBAN']))
print('Статус строки в этом списке:', is_contains('cycle', ['recycling', 'cyclic']))

print('Общее количество вызовов функции:', calls)