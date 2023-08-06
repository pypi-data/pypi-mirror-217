import time


class Timer:
    """A timer context for easily timing blocks of code.

    Args:
        accumulate: Whether to accumulate time over multiple context entries
                    A value of `False` means timer is reset each time the
                    context is entered.

    Example:
        timer = Timer()

        with timer:
            do_something
            do_something_else
        print(timer.time)              # print the time taken
        print(timer.as_dict)           # prints {"time": time_taken}

        timer = Timer(True)     # accumulate time
        with timer:
            do_something

        with timer:             # doesn't reset
            do_something_else

        print(timer.time)
        timer.clear()           # now reset
    """
    def __init__(self, accumulate: bool = False):
        self._accumulate: bool = accumulate
        self._time = 0

    def __enter__(self):
        self._start = time.time()

    def __exit__(self, *args):
        self._last = time.time() - self._start
        if self.accumulate:
            self._time += self._last
        else:
            self._time = self._last

    def clear(self):
        "Clear the timer instance"
        self._time = 0

    @property
    def last(self) -> float:
        """Return the last measured time

        Same as :attr:`time` if :attr:`accumulate` is false

        """
        return self._last

    @property
    def time(self) -> float:
        "Return the time"
        return self._time

    @property
    def accumulate(self) -> bool:
        "Are we accumulating the times?"
        return self._accumulate

    @property
    def as_dict(self):
        "As a dictionary of {\"time\": time}"
        return {"time": self._time}
