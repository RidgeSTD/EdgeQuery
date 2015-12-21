from copy import deepcopy

from common import QueryBox

def main():
    a = QueryBox(0)
    a.candidate = {2:[4]}
    b = QueryBox(1)
    b.candidate = deepcopy(a.candidate)
    # b.candidate = a.candidate.copy()
    # b.candidate[2].append(5)
    print(a.candidate)




def safea(stack, t, data):
    new_t = t + 1
    if len(stack) <= new_t:
        print('extend!')
        stack.extend([0 for i in range(0, min(len(stack), 1))])
    stack[new_t] = data
    return new_t



if __name__ == "__main__":
    main()
