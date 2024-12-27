import collections
import operator
import random


def builtins():
    x = [1, None, 2, 3]
    for y in filter(x):
        ...  # y = 1, then y = 2, then y = 3


def powers_of_2():
    val = 1
    while True:
        yield val
        val *= 2


def you_can_make_any_itertool(it):
    for x in it:
        ...
        yield ...


import itertools


def dot_product(u, v):
    pairs = zip(u, v, strict=True)  # (u0, v0) (u1, v1) ...
    products = itertools.starmap(operator.mul, pairs)  # u0*v0 u1*v1 ...
    result = sum(products)  # u0*v0 + u1*v1 ...
    return result


def dot_product_better(u, v):
    total = 0
    for x, y in zip(u, v, strict=True):
        total += x * y

    return total


def multi_accumulate(iterable, *functions):
    """
    multi_accumulate([1, -1, 2, -2], min, max) ->
     (1, 1) (-1, 1) (-1, 2) (-2, 2)
    """

    def multi_update(lasts, x):
        return tuple(f(last, x) for f, last in zip(functions, lasts))

    iterator = iter(iterable)
    try:
        initial = next(iterator)
    except StopIteration:
        return
    yield from itertools.accumulate(
        iterable,
        multi_update,
        initial=tuple(initial for _ in range(len(functions))),
    )


def last_element(iterable):
    deque = collections.deque(iterable, maxlen=1)  # faster than for loop
    if not deque:
        raise ValueError("empty iterable")
    return deque[0]


def multi_reduce(iterable, *functions):
    return last_element(multi_accumulate(iterable, *functions))


def min_max(iterable):
    return multi_reduce(iterable, min, max)


def main():
    iterable = [random.randint(-10, 10) for _ in range(100)]
    functions = min, max, operator.add, operator.mul, lambda x, y: y

    for result in multi_accumulate(iterable, *functions):
        print(result)


if __name__ == "__main__":
    main()
