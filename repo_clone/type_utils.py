def add_one(x):
    if isinstance(x, int):
        return x + 1
    elif isinstance(x, str):
        return x + "1"
    else:
        raise TypeError("Input must be an int or str")

print(add_one("hello"))