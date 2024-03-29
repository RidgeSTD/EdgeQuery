import copy
import time
import cProfile
import common
import statics
from data_structure_util import CQueue

__author__ = 'alex'

head_map = None
END = 0
dfs_exit = 0


def entrance(in_tree, out_tree, twigs, l_in, l_out, node_set, q_in, q_out, q_in_menu, q_out_menu, fo):
    global head_map, END

    heads = []
    END = len(twigs)
    for twig in twigs:
        heads.append(twig.head)
    print("开始获取head映射...")
    print("开始获取head映射...", file=statics.f_console)
    t1 = time.clock()  # timer
    result = __get_head_map(in_tree, out_tree, heads, q_in, q_out, q_in_menu, q_out_menu)
    t2 = time.clock()  # timer
    print("获取head映射耗时 " + str(t2 - t1))
    print("获取head映射耗时 " + str(t2 - t1), file=statics.f_console)

    # 对照, 朴素的head获取方法
    __naive_get_head_map(l_in, l_out, node_set, heads, q_in, q_out)

    if result == common.INVALID_CANDIDATE:
        return common.INVALID_CANDIDATE
    querybox_list = CQueue()
    querybox_list.put(common.QueryBox(0))
    print("查询内核启动...")
    print("查询内核启动...", file=statics.f_console)
    t3 = time.clock()  # timer
    while not querybox_list.is_empty():
        x_box = querybox_list.get()
        result = __core(l_in=l_in, l_out=l_out, box=x_box, twigs=twigs, fo=fo)
        for each in result:
            querybox_list.put(each)
    t4 = time.clock()  # timer
    print("查询内核运行耗时 " + str(t4 - t3))
    print("查询内核运行耗时 " + str(t4 - t3), file=statics.f_console)


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


def __naive_get_head_map(l_in, l_out, node_set, heads, q_in, q_out):
    print("naive的head查询开始...")
    print("naive的head查询开始...", file=statics.f_console)
    t_st_naive = time.clock()
    n_head_map = {}
    for head in heads:
        n_head_map[head] = set()
        for node in node_set:
            flag = True
            if head in q_in:
                for l in q_in[head]:
                    if node not in l_in or l not in l_in[node] or l_in[node] < q_in[head]:
                        flag = False
                        break
            if head in q_out:
                for l in q_out[head]:
                    if node not in l_out or l not in l_out[node] or l_out[node] < q_out[head]:
                        flag = False
                        break
            if flag:
                n_head_map[head].add(node)
    t_en_naive = time.clock()
    print("naive的head查询运行耗时 " + str(t_en_naive - t_st_naive))
    print("naive的head查询运行耗时 " + str(t_en_naive - t_st_naive), file=statics.f_console)


def __locate_node(head, q_edge, q_menu, tree):
    global dfs_exit

    statics.locate_called_time += 1
    statics.locate_dfs_recirsive_call = 0
    tt1 = time.clock()
    if head not in q_menu:
        return [tree]
    dfs_exit = len(q_menu[head])
    result = __dfs_locate_node(x=tree, step=0, step_count=1, q_edge=q_edge, q_menu=q_menu, head=head)

    print("本次locate_dfs递归次数:" + str(statics.locate_dfs_recirsive_call))
    print("本次locate_dfs递归次数:" + str(statics.locate_dfs_recirsive_call), file=statics.f_console)
    statics.located_run_time += time.clock() - tt1
    if not result:
        return common.INVALID_CANDIDATE
    return result


def __dfs_locate_node(x, step, step_count, q_edge, q_menu, head):
    global dfs_exit

    statics.locate_dfs_recirsive_call += 1

    if step >= dfs_exit:
        return set({x})
    if not x.label_menu:
        return set()

    result = set()

    for l in x.label_menu:
        if l > q_menu[head][step][0]:
            break
        elif l == q_menu[head][step][0]:
            if step_count == q_menu[head][step][1]:
                result.update(__dfs_locate_node(x.children[l], step + 1, 1, q_edge, q_menu, head))
            else:
                result.update(__dfs_locate_node(x.children[l], step, step_count + 1, q_edge, q_menu, head))
        elif q_menu[head][step][0] in x.children[l].prophecy:
            result.update(__dfs_locate_node(x.children[l], step, step_count, q_edge, q_menu, head))

    return result


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

    t1 = time.clock()  # timer
    can_list = list(candidate)
    ESC = len(can_list)
    buf = {}
    iter(0)
    t2 = time.clock()  # timer
    statics.ans_io_time += (t2 - t1)
