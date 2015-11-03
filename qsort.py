__author__ = 'alex'

def qsort(arr, st, en):
    l = st
    r = en
    mid = arr[int((st+en)/2)]
    while True:
        while arr[l]<mid:
            l+=1
        while arr[r]>mid:
            r-=1
        if l<=r:
            tmp = arr[l]
            arr[l] = arr[r]
            arr[r] = tmp
            l+=1
            r-=1
        if r<l:
            break
    if st<r:
        qsort(arr, st, r)
    if l<en:
        qsort(arr, l, en)

print("start...")
a = [1,5,22,6,7,2,1]
qsort(a, 0, len(a)-1)
print(a)

