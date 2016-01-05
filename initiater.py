import statics
from common import TreeNode
import time

__author__ = 'alex'


def init_in_out_tree(l_in, l_out, l_in_menu, l_out_menu, node_set):
    in_table, out_table = __build_in_out_table(l_in, l_out, l_in_menu, l_out_menu)
    in_tree, out_tree = __build_in_out_tree(in_table, out_table, l_in_menu, l_out_menu, node_set)
    return in_tree, out_tree


def __build_in_out_table(l_in, l_out, l_in_menu, l_out_menu):
    print("开始构建出入度表...")
    print("开始构建出入度表...", file=statics.f_cons)
    t1 = time.clock()
    in_table = {}
    out_table = {}
    for node in l_in:
        in_table[node] = {}
        for label in l_in_menu[node]:
            in_table[node][label] = len(l_in[node][label])
    for node in l_out:
        out_table[node] = {}
        for label in l_out_menu[node]:
            out_table[node][label] = len(l_out[node][label])
    t2 = time.clock()
    print("构建出入度表耗时 " + str(t2 - t1))
    print("构建出入度表耗时 " + str(t2 - t1), file=statics.f_cons)
    return in_table, out_table


def __build_in_out_tree(in_table, out_table, l_in_menu, l_out_menu, node_set):
    print("开始构建出入度树...")
    print("开始构建出入度树...", file=statics.f_cons)
    t1 = time.clock()
    in_tree = __build_tree(in_table, l_in_menu, node_set)
    out_tree = __build_tree(out_table, l_out_menu, node_set)
    t2 = time.clock()
    print("构建出入度树耗时 " + str(t2 - t1))
    print("构建出入度树耗时 " + str(t2 - t1), file=statics.f_cons)
    return in_tree, out_tree


def __build_tree(table, menu, node_set):
    root = TreeNode(data=[])
    for node in node_set:
        pin = root
        if node not in menu:
            root.data.append(node)
            continue
        if not menu[node]:
            root.data.append(node)
            continue

        for label in menu[node]:
            for i in range(0, table[node][label]):
                if label not in pin.children:
                    child = TreeNode(data=[])
                    pin.add_child(label, child)
                    pin = child
                else:
                    pin = pin.children[label]
        pin.data.append(node)

    # 梳理树中的目录信息
    q = [root]
    h = 0
    t = 0
    while h <= t:
        q[h].label_menu.sort()
        for edge in q[h].children:
            q.append(q[h].children[edge])
        t += len(q[h].children)
        h += 1

    return root


def __mearge_array(a1, a2):
    """
    merge two sorted array into one sorted array
    """
    if len(a1) < 1:
        return a2
    if len(a2) < 1:
        return a1
    p1 = 0
    p2 = 0
    l1 = len(a1)
    l2 = len(a2)
    tmp = [0]
    t = -1
    while p1 < l1 and p2 < l2:
        if a1[p1] < a2[p2]:
            t = safe_push(tmp, t, a1[p1])
            while True:
                p1 += 1
                if p1 >= l1 or a1[p1] > a1[p1 - 1]:
                    break
        elif a1[p1] == a2[p2]:
            t = safe_push(tmp, t, a1[p1])
            while True:
                p1 += 1
                if p1 >= l1 or a1[p1] > a1[p1 - 1]:
                    break
            while True:
                p2 += 1
                if p2 >= l2 or a2[p2] > a2[p2 - 1]:
                    break
        else:
            t = safe_push(tmp, t, a2[p2])
            while True:
                p2 += 1
                if p2 >= l2 or a2[p2] > a2[p2 - 1]:
                    break
    while p1 < l1:
        t = safe_push(tmp, t, a1[p1])
        p1 += 1
    while p2 < l2:
        t = safe_push(tmp, t, a2[p2])
        p2 += 1
    return tmp[0: t + 1]


def safe_push(stack, t, data):
    """
    take the input stack and the top pointer t
    double the size of stack if stack overflow
    return the new top pointer. *NOTE TO receive the new pointer!*
    """
    new_t = t + 1
    if len(stack) <= new_t:
        stack.extend([0 for i in range(0, len(stack))])
    stack[new_t] = data
    return new_t
