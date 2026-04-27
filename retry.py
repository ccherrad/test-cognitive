import time


def retry(func, attempts=3, delay=1):
    for i in range(attempts):
        try:
            return func()
        except Exception as e:
            if i == attempts - 1:
                raise
            time.sleep(delay)


if __name__ == "__main__":
    calls = {"count": 0}

    def flaky():
        calls["count"] += 1
        if calls["count"] < 3:
            raise ValueError("not ready yet")
        return "success"

    print(retry(flaky))
