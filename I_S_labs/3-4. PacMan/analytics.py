import time
from functools import wraps
import counters


def increaseCounter():
    counters.counter += 1


def increaseTotalTime(iterationTime):
    counters.totalTime += iterationTime


def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        increaseCounter()
        increaseTotalTime(t1 - t0)
        print("Current iteration execution time: ", t1 - t0, "s seconds")
        print("Total time running %s: %s seconds" %
              (function.__name__, str(counters.totalTime))
              )
        print("Iterations count: ", counters.counter)
        return result

    return function_timer
