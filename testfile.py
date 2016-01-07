import math
import copy
from time import clock
import common
import test2
import cProfile


def foo(x):
    if x > 995:
        print('bottom!')
        return
    foo(x+1)


def main():
    foo(1)


if __name__ == "__main__":
    main()