import statics
import time
from common import TreeNode
from common import intersect
from data_structure_util import CQueue

__author__ = 'alex'


def init_in_out_tree(l_in, l_out, l_in_menu, l_out_menu, node_set, neighbor):
    in_table, out_table = __build_in_out_table(l_in, l_out, l_in_menu, l_out_menu)
    in_tree, out_tree = __build_in_out_tree(in_table, out_table, l_in_menu, l_out_menu, node_set, neighbor)
    return in_tree, out_tree


def __build_in_out_table(l_in, l_out, l_in_menu, l_out_menu):
    print("开始构建出入度表...")
    print("开始构建出入度表...", file=statics.f_cons)
    t1 = time.clock()  # timer
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
    t2 = time.clock()  # timer
    print("构建出入度表耗时 " + str(t2 - t1))
    print("构建出入度表耗时 " + str(t2 - t1), file=statics.f_cons)
    return in_table, out_table


def __build_in_out_tree(in_table, out_table, l_in_menu, l_out_menu, node_set, neighbor):
    print("开始构建出入度树...")
    print("开始构建出入度树...", file=statics.f_cons)
    t1 = time.clock()  # timer
    statics.io_tree_node_count = 0
    in_tree = __build_tree(in_table, l_in_menu, node_set, neighbor)
    out_tree = __build_tree(out_table, l_out_menu, node_set, neighbor)
    t2 = time.clock()  # timer
    print("构建出入度树耗时 " + str(t2 - t1))
    print("构建出入度树耗时 " + str(t2 - t1), file=statics.f_cons)
    print("出入度树节点数共计 " + str(statics.io_tree_node_count + 1))
    print("出入度树节点数共计 " + str(statics.io_tree_node_count + 1), file=statics.f_cons)
    return in_tree, out_tree


def __build_tree(table, menu, node_set, neighbor):
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

    print("开始调整出入度树以最大化差异...")
    print("开始调整出入度树以最大化差异...", file=statics.f_cons)
    # 梳理树中的目录信息, 并根据邻居信息将树中同一树节点上的点按照最大novelty间隔排开
    q = CQueue()
    q.put(root)
    t_start_intervein = time.clock()
    while not q.is_empty():
        x_node = q.get()
        __intervein_node(x_node.data, neighbor)
        x_node.label_menu.sort()
        for edge in x_node.children:
            q.put(x_node.children[edge])
    t_end_intervein = time.clock()
    print("差异化出入度表耗时 " + str(t_end_intervein - t_start_intervein))
    print("差异化出入度表耗时 " + str(t_end_intervein - t_start_intervein), file=statics.f_cons)

    return root


def __intervein_node(node_list, neighbor):
    """
    -->计算余弦相似度并间隔岔开. 此处可以GPU加速
    """
    # TODO
    for i in range(0, len(node_list) - 1):
        max_cos_d = -9999
        mark = 0
        for j in range(i + 1, len(node_list)):
            tmp = __cal_cos_diff(neighbor[node_list[i]].in_nodes,
                                 neighbor[node_list[i]].in_nodes_menu,
                                 neighbor[node_list[i]].in_module,
                                 neighbor[node_list[j]].in_nodes,
                                 neighbor[node_list[j]].in_nodes_menu,
                                 neighbor[node_list[j]].in_module)
            if tmp > max_cos_d:
                max_cos_d = tmp
                mark = j
        if i + 1 != mark:
            tmp = node_list[i + 1]
            node_list[i + 1] = node_list[mark]
            node_list[mark] = tmp


def __cal_cos_diff(dic1, menu1, mod1, dic2, menu2, mod2):
    """

    Get the inner product of two vectors

    :param dic1: Value of dimensions of first vector
    :param menu1: dimensions of first vector
    :param mod1: module of first vector
    :param dic2: Value of dimensions of second vector
    :param menu2: dimensions of second vector
    :param mod2: module of second vector
    """
    if mod1 == 1 or mod2 == 0:
        return 0
    intersection = menu1.intersection(menu2)
    tmp = 0
    for node in intersection:
        tmp += dic1[node] * dic2[node]
    tmp /= mod1 * mod2
    return tmp
