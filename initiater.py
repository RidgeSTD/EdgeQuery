__author__ = 'alex'

from common import TreeNode


def build_in_out_table(l_in, l_out, l_in_menu, l_out_menu):
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


def build_tree(table, menu):
    root = TreeNode(data=[])
    for node in table:
        pin = root
        for label in menu[node]:
            for i in range(0, table[node][label]):
                if label not in pin.children:
                    child = TreeNode(data=[])
                    pin.add_child(label, child)
                    pin = child
                else:
                    pin = pin.children[label]
        pin.data.append(node)
    return root


def build_in_out_tree(in_table, out_table, l_in_menu, l_out_menu):
    in_tree = build_tree(in_table, l_in_menu)
    out_tree = build_tree(out_table, l_out_menu)
    return in_tree, out_tree


def init_in_out_tree(l_in, l_out, l_in_menu, l_out_menu):
    in_table, out_table = build_in_out_table(l_in, l_out, l_in_menu, l_out_menu)
    in_tree, out_tree = build_in_out_tree(in_table, out_table, l_in_menu, l_out_menu)
    return in_tree, out_tree
