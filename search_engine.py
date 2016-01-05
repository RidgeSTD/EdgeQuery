import copy
import time

import common
import statics
__author__ = 'alex'

head_map = None
END = 0


def entrance(in_tree, out_tree, twigs, l_in, l_out, q_in, q_out, q_in_menu, q_out_menu, fo):
    global head_map, END

    heads = []
    END = len(twigs)
    for twig in twigs:
        heads.append(twig.head)
    print("开始获取head映射...")
    print("开始获取head映射...", file=statics.f_cons)
    t1 = time.clock()
    result = __get_head_map(in_tree, out_tree, heads, q_in, q_out, q_in_menu, q_out_menu)
    t2 = time.clock()
    print("获取head映射耗时 " + str(t2 - t1))
    print("获取head映射耗时 " + str(t2 - t1), file=statics.f_cons)
    if result == common.INVALID_CANDIDATE:
        return common.INVALID_CANDIDATE
    querybox_list = [common.QueryBox(0)]
    h = 0
    t = 1
    print("查询内核启动...")
    print("查询内核启动...", file=statics.f_cons)
    t3 = time.clock()
    while h < t:
        result = __core(l_in=l_in, l_out=l_out, box=querybox_list[h], twigs=twigs, fo=fo)
        querybox_list.extend(result)
        t += len(result)
        h += 1
    t4 = time.clock()
    print("查询内核运行耗时 " + str(t4 - t3))
    print("查询内核运行耗时 " + str(t4 - t3), file=statics.f_cons)


def __get_head_map(in_tree, out_tree, heads, q_in, q_out, q_in_menu, q_out_menu):
    global head_map

    head_map = {}
    for head in heads:
        result = __locate_node(head, q_in, q_in_menu, in_tree)
        if result == common.INVALID_CANDIDATE:
            return common.INVALID_CANDIDATE
        in_set = set()
        for tree_node in result:
            in_set = in_set.union(tree_node.get_subtree_node_set())

        result = __locate_node(head, q_out, q_out_menu, out_tree)
        if result == common.INVALID_CANDIDATE:
            return common.INVALID_CANDIDATE
        out_set = set()
        for tree_node in result:
            out_set = out_set.union(tree_node.get_subtree_node_set())

        head_map[head] = in_set.intersection(out_set)
    return head_map


def __locate_node(head, q_edge, q_menu, tree):
    class block:
        def __init__(self, cursor, step):
            self.cursor = cursor
            self.step = step

    if head not in q_menu:
        return [tree]

    q = [block(cursor=tree, step=(0, 1))]
    ans_list = []
    h = 0
    t = 0
    ESC = len(q_menu[head])
    while h <= t:
        q_label = q_menu[head][q[h].step[0]][0]
        for i in range(0, len(q[h].cursor.label_menu)):
            tree_label = q[h].cursor.label_menu[i]
            if tree_label > q_label:
                break
            elif tree_label == q_label:
                if q[h].step[0] == ESC - 1 and q[h].step[1] >= q_menu[head][q[h].step[0]][1]:
                    ans_list.append(q[h].cursor.children[tree_label])
                    continue
                if q[h].step[1] >= q_menu[head][q[h].step[0]][1]:
                    q.append(block(cursor=q[h].cursor.children[tree_label], step=(q[h].step[0] + 1, 1)))
                else:
                    q.append(block(cursor=q[h].cursor.children[tree_label], step=(q[h].step[0], q[h].step[1] + 1)))
                t += 1
            else:
                q.append(block(cursor=q[h].cursor.children[tree_label], step=q[h].step))
                t += 1
        h += 1
    if not ans_list:
        return common.INVALID_CANDIDATE
    else:
        return ans_list


def __core(l_in, l_out, box, twigs, fo):
    global head_map, END

    if box.step >= END:
        __print_ans(box.candidate, fo)
        return []
    twig = twigs[box.step]
    tmp_list = []
    for head_candidate in head_map[twig.head]:
        new_box = common.QueryBox(box.step + 1)
        new_box.candidate = copy.deepcopy(box.candidate)
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


def __print_ans(candidate, fo):
    def iter(step):
        if step >= ESC:
            s = ""
            for q_node in buf:
                s += (str(q_node) + " = " + str(buf[q_node]) + ",\t")
            s += '\n'
            fo.write(s)
            # print(s)
            return
        for can in candidate[can_list[step]]:
            buf[can_list[step]] = can
            iter(step + 1)

    t1 = time.clock()
    can_list = list(candidate)
    ESC = len(can_list)
    buf = {}
    iter(0)
    t2 = time.clock()
    statics.ans_io_time += (t2 - t1)
