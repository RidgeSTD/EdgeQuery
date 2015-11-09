import common


__author__ = 'alex'


head_map = None
END = 0


def entrance(in_tree, out_tree, twigs, l_in, l_out, q_in, q_out, q_in_menu, q_out_menu):
    global head_map, END

    heads = []
    END = len(twigs)
    for twig in twigs:
        heads.append(twig.head)
    result = __get_head_map(in_tree, out_tree, heads, q_in, q_out, q_in_menu, q_out_menu)
    if result == common.INVALID_CANDIDATE:
        return common.INVALID_CANDIDATE
    querybox_list = [common.QueryBox(0)]
    h = 0
    t = 1
    while h < t:
        result = __core(l_in=l_in, l_out=l_out, box=querybox_list[h], twigs=twigs)
        querybox_list.extend(result)
        t += len(result)
        h += 1


def __get_head_map(in_tree, out_tree, heads, q_in, q_out, q_in_menu, q_out_menu):
    global head_map

    head_map = {}
    for head in heads:
        result = __locate_node(head, q_in, q_in_menu, in_tree)
        if result == common.INVALID_CANDIDATE:
            return common.INVALID_CANDIDATE
        in_set = result.get_subtree_node_set()

        result = __locate_node(head, q_out, q_out_menu, out_tree)
        if result == common.INVALID_CANDIDATE:
            return common.INVALID_CANDIDATE
        out_set = __locate_node(head, q_out, q_out_menu, out_tree).get_subtree_node_set()

        head_map[head] = in_set.intersection(out_set)
    return head_map


def __locate_node(head, q_edge, q_menu, tree):
    cursor = tree
    if head not in q_menu:
        return cursor
    for label, count in q_menu[head]:
        for i in range(0, count):
            try:
                cursor = cursor.children[label]
            except KeyError:
                return common.INVALID_CANDIDATE
    return cursor


def __core(l_in, l_out, box, twigs):
    global head_map, END

    if box.step >= END:
        __print_ans(box.candidate)
        return []
    twig = twigs[box.step]
    tmp_list = []
    for head_candidate in head_map[twig.head]:
        new_box = common.QueryBox(box.step + 1)
        new_box.candidate = box.candidate.copy()
        if twig.head in new_box.candidate and head_candidate not in new_box.candidate[twig.head]:
            continue
        new_box.candidate[twig.head] = {head_candidate}

        result = common.VALID_CANDIDATE
        for label, ori in twig.in_edge:
            result = new_box.adapt_candidates({ori: set(l_in[head_candidate][label])}, filter_afterwards=True)
            if result == common.INVALID_CANDIDATE:
                break
        if result == common.INVALID_CANDIDATE:
            continue

        result = common.VALID_CANDIDATE
        for label, des in twig.out_edge:
            result = new_box.adapt_candidates({des: set(l_out[head_candidate][label])}, filter_afterwards=True)
            if result == common.INVALID_CANDIDATE:
                break
        if result == common.INVALID_CANDIDATE:
            continue

        tmp_list.append(new_box)
    return tmp_list


def __print_ans(candidate):
    print(candidate)
