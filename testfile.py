import math
import copy
from time import clock
import common


def main():
    b = [1, 2, 3, 4, 8, 9, 10, 11]
    c = [1, 2, 3, 4, 8, 9, 10, 11]
    a = [7, 100, 101, 102]
    d = [7, 100, 101, 102]
    sa = set(a)
    sb = set(b)
    aa = 0
    print('===========循环访问=============')
    t1 = clock()
    for i in range(1, 10000):
        for j in range(0, len(a)):
            t = a[j]
        for j in range(0, len(b)):
            t = b[j]
        aa = t
    print(clock() - t1)
    print('===========extend=============')
    t1 = clock()
    for i in range(1, 10000):
        c.extend(d)
        c = [1, 2, 3, 4, 8, 9, 10, 11]
    print(clock() - t1)
    print('==========我并系统并==============')
    t1 = clock()
    for i in range(1, 10000):
        common.union(a, b)
    print(clock() - t1)

    t1 = clock()
    for i in range(1, 10000):
        sa = set(a)
        sb = set(b)
        sa.union(sb)
    print(clock() - t1)
    print('========我交系统交================')
    t1 = clock()
    for i in range(1, 10000):
        common.intersect(a, b)
    print(clock() - t1)

    t1 = clock()
    for i in range(1, 10000):
        sa = set(a)
        sb = set(b)
        sa.intersection(sb)
    print(clock() - t1)


if __name__ == "__main__":
    main()