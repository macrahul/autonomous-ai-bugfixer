def add_one(x):
    if isinstance(x, int):
        return x + 1
    elif isinstance(x, str):
        return x + "1"
    else:
        raise TypeError("Unsupported type")

print(add_one("hello"))