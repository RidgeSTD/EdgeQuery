import time
a = set()
a.add(1)
a.add(3)
a.add(4)
a.add(5)
b = set()
b.add(1)
b.add(0)
b.add(3)
b.add(7)
b.add(5)
print(a)
print(b)

t1 = time.clock()
for i in range(1, 1000000):
    # print(a.intersection(b))
    c = a.intersection(b)
t2 = time.clock()
print(str(t2-t1))

