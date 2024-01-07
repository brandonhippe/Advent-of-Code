import time


class Timer:
    def __init__(self, suppress = False) -> None:
        self.t0 = 0
        self.t1 = 0
        self.elapsed = 0
        self.suppress = suppress

    def __enter__(self):
        self.t0 = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            return None
        else:
            self.t1 = time.perf_counter()
            self.elapsed = self.t1 - self.t0

        return self.elapsed