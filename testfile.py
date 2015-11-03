__author__ = 'alex'
import time
import random

global arr

def qsort(xs):
    if len(xs) <= 0:
        return []
    return qsort([x for x in xs[1:] if x > xs[0]]) + \
            [xs[0]] + \
           qsort([x for x in xs[1:] if x <= xs[0]])

arr = []
t = time.clock()
print("start generate array at "+str(t))
for i in range(0, 5):
    arr.append(random.randint(1, 100))
t2 = time.clock()
print("end generating array at "+str(t2)+" elapse: "+str(t2-t))

t = time.clock()
print("start at "+str(t))
arr.sort()
t2 = time.clock()
print("end sorting at "+str(t2)+" elapse: "+str(t2-t))
print(arr)

######
t = time.clock()
print("start generate array at "+str(t))
for i in range(0, 5):
    arr.append(random.randint(1, 100))
t2 = time.clock()
print("end generating array at "+str(t2)+" elapse: "+str(t2-t))

t = time.clock()
print("start at "+str(t))
arr = qsort(arr)
t2 = time.clock()
print("end sorting at "+str(t2)+" elapse: "+str(t2-t))
print(arr)