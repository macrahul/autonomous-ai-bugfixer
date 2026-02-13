def add_one(x):
    if isinstance(x, str):
        return x + "1"
    return x + 1

print(add_one("hello"))