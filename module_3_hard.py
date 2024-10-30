def calculate_structure_sum(*args):
    total_sum = 0

    for data in args:
        if isinstance(data, (list, tuple, set)):
            total_sum += calculate_structure_sum(*data)
        elif isinstance(data, dict):
            for key, value in data.items():
                total_sum += calculate_structure_sum(key)
                total_sum += calculate_structure_sum(value)
        elif isinstance(data, str):
            total_sum += len(data)
        elif isinstance(data, (int, float)):
            total_sum += data

    return total_sum


data_structure = [
    [1, 2, 3],
    {'a': 4, 'b': 5},
    (6, {'cube': 7, 'drum': 8}),
    "Hello",
    ((), [{(2, 'Urban', ('Urban2', 35))}])
]

result = calculate_structure_sum(*data_structure)
print(result)