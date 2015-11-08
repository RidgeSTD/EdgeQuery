__author__ = 'alex'


import common


def entrance(in_tree, out_tree, twigs, q_in, q_out, q_in_menu, q_out_menu):
    heads = []
    for twig in twigs:
        heads.append(twig.head)
    head_map = __get_head_map(in_tree, out_tree, heads, q_in, q_out, q_in_menu, q_out_menu)
    print(head_map)
    pass


def __get_head_map(in_tree, out_tree, heads, q_in, q_out, q_in_menu, q_out_menu):
    head_map = {}
    for head in heads:
        in_set = __search_node(head, q_in, q_in_menu, in_tree).get_subtree_node_set()
        out_set = __search_node(head, q_out, q_out_menu, out_tree).get_subtree_node_set()
        head_map[head] = in_set.intersection(out_set)
    return head_map


def __search_node(head, q_edge, q_menu, tree):
    cursor = tree
    if head not in q_menu:
        return cursor
    for label, count in q_menu[head]:
        for i in range(0, count):
            try:
                cursor = cursor.children[label]
            except KeyError:
                return common.INVALIDATE_CANDIDATE
    return cursor


def __core(in_tree, out_tree, box):
    pass