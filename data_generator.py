from random import *


def main():
    k_node_100k_edge(2000)
    pass


def k_node_100k_edge(tag_size):
    f = open('/Users/alex/g_data.txt', 'a')
    for i in range(0, 10000000):
        ori = randint(0, 100000)
        des = randint(0, 100000)
        while des == ori:
            des = randint(0, 100000)
        edg = randint(0, tag_size)
        s = str(ori) + '\t' + str(edg) + '\t' + str(des) + '\n'
        f.write(s)
    f.close()


if __name__ == "__main__":
    main()
