import math
import copy
from time import clock
import common
import test2
import cProfile
import time
import timeit


def foo(x):
    if x > 995:
        print('bottom!')
        return
    foo(x+1)


def main():
    b = set([1, 2, 3])
    print(b)
    print(2 in b)


if __name__ == "__main__":
    main()