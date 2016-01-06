import math
import copy

def __dimidiate_search(val, l, r, arr):
    st = l - 1
    en = r + 1
    while st < en - 1:
        mid = math.floor((st + en)/2)
        if arr[mid] < val:
            st = mid
        else:
            en = mid
    return en


def main():
    a = [1, 2, 3, 4, 5]
    # print(__dimidiate_search(0, 0, 4, a))
    tmp = copy.deepcopy(a[2:5])
    tmp2 = a[0:5]
    print(tmp)
    print(id(a))
    print(id(tmp))
    print(id(tmp2))
    print(id(a[2:5]))
    a[2] = 200
    print(tmp2)


if __name__ == "__main__":
    main()