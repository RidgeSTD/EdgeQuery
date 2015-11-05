import time

a = set()
t1 = time.clock()
for i in range(0, 1000000):
    a.add(i)
t2 = time.clock()
print('add set elapse for:'+str(t2-t1))

t1 = time.clock()
for i in range(0, 100):
    a = a.union(a)
t2 = time.clock()
print('len elapse for:'+str(t2-t1))