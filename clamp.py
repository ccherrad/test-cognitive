def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))


if __name__ == "__main__":
    print(clamp(15, 0, 10))
    print(clamp(-5, 0, 10))
    print(clamp(7, 0, 10))
