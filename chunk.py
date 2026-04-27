def chunk(items: list, size: int) -> list:
    return [items[i:i + size] for i in range(0, len(items), size)]


if __name__ == "__main__":
    data = list(range(10))
    print(chunk(data, 3))
