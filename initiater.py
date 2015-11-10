from common import TreeNode

__author__ = 'alex'


def init_in_out_tree(l_in, l_out, l_in_menu, l_out_menu, node_set):
    in_table, out_table = __build_in_out_table(l_in, l_out, l_in_menu, l_out_menu)
    in_tree, out_tree = __build_in_out_tree(in_table, out_table, l_in_menu, l_out_menu, node_set)
    return in_tree, out_tree


def __build_in_out_table(l_in, l_out, l_in_menu, l_out_menu):
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
    return in_table, out_table


def __build_in_out_tree(in_table, out_table, l_in_menu, l_out_menu, node_set):
    in_tree = __build_tree(in_table, l_in_menu, node_set)
    out_tree = __build_tree(out_table, l_out_menu, node_set)
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



