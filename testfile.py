def main():
    a = [1, 2, 3, 4]
    t = 2
    print(a[t])
    print(a[0: t+1])


def safea(stack, t, data):
    new_t = t + 1
    if len(stack) <= new_t:
        print('extend!')
        stack.extend([0 for i in range(0, min(len(stack), 1))])
    stack[new_t] = data
    return new_t



if __name__ == "__main__":
    main()
