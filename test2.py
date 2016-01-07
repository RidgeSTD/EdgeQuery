import cProfile


def foo1():
    pow(2, 20)


def foo2():
    cProfile.run(statement='foo1()')
