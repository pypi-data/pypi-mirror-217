def read(path: str):
    with open(path, encoding="utf-8") as file:
        return file.read()


def write(path: str, data):
    with open(path, mode='w') as file:
        return file.write(data)


def append(path: str, data):
    with open(path, mode='a') as file:
        return file.write(data)
