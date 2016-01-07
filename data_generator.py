from random import *
import os

from common import ROOT_PATH


def main():
    k_node_100k_edge(40)
    pass


def k_node_100k_edge(tag_size):
    if os.path.isfile(ROOT_PATH + 'g_data.txt'):
        os.remove(ROOT_PATH + 'g_data.txt')

    f = open(ROOT_PATH + 'g_data.txt', 'a')
    for i in range(0, 10000):
        ori = randint(0, 700)
        des = randint(0, 700)
        while des == ori:
            des = randint(0, 700)
        edg = randint(0, tag_size)
        s = str(ori) + '\t' + str(edg) + '\t' + str(des) + '\n'
        f.write(s)
    f.close()


if __name__ == "__main__":
    main()
