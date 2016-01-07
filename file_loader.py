import time

import statics
from common import ROOT_PATH
from common import NeighborInfo
from data_structure_util import CQueue

__author__ = 'alex'


def load_map():
    """
    Pass L_in, L_out, noted for in/out degree dictionary and in/out label-marked dictionary

    NOTE! The initialization must be done outside the function
    """
    print("开始加载文件...")
    print("开始加载文件...", file=statics.f_cons)
    t_start_load_file = time.clock()  # timer
    l_in = {}
    l_out = {}
    l_in_menu = {}
    l_out_menu = {}
    node_set = set()
    f = open(ROOT_PATH + "data.txt")
    while True:
        line = f.readline()
        if len(line) < 1:
            break
        tpl = line.split('\t')
        ori = int(tpl[0])
        edg = int(tpl[1])
        des = int(tpl[2])

        node_set.add(ori)
        node_set.add(des)

        if ori not in l_out:
            l_out[ori] = {}
        if ori not in l_out_menu:
            l_out_menu[ori] = []
        if des not in l_in:
            l_in[des] = {}
        if des not in l_in_menu:
            l_in_menu[des] = []

        try:
            l_in[des][edg].append(ori)
        except:
            l_in[des][edg] = []
            l_in[des][edg].append(ori)

        try:
            l_out[ori][edg].append(des)
        except:
            l_out[ori][edg] = []
            l_out[ori][edg].append(des)

        if edg not in l_in_menu[des]:
            l_in_menu[des].append(edg)
        if edg not in l_out_menu[ori]:
            l_out_menu[ori].append(edg)
    f.close()
    t_end_load_file = time.clock()  # timer
    print("结束加载文件...")
    print("结束加载文件...", file=statics.f_cons)
    print('加载文件耗时 ' + str(t_end_load_file - t_start_load_file))
    print('加载文件耗时 ' + str(t_end_load_file - t_start_load_file), file=statics.f_cons)

    t_start_sort_raw_data = time.clock()  # timer
    __inner_sort(l_in, l_in_menu)
    __inner_sort(l_out, l_out_menu)
    t_end_sort_raw_data = time.clock()  # timer
    print("原始数据内部排序耗时 " + str(t_end_sort_raw_data - t_start_sort_raw_data))
    print("原始数据内部排序耗时 " + str(t_end_sort_raw_data - t_start_sort_raw_data), file=statics.f_cons)

    print("开始统计邻居信息")
    print("开始统计邻居信息", file=statics.f_cons)
    t_start_neighbor = time.clock()  # timer
    # 统计邻居节点信息
    neighbor = {}
    # 先统计入度
    visited = set()
    q_node = CQueue()
    q_dep = CQueue()
    for node in node_set:
        visited.clear()
        visited.add(node)
        neighbor[node] = NeighborInfo()
        q_node.clear()
        q_dep.clear()
        q_node.put(node)
        q_dep.put(0)
        while not q_node.is_empty():
            x_node = q_node.get()
            x_dep = q_dep.get()
            next_dep = x_dep + 1
            if x_node not in l_in:
                continue
            for l in l_in[x_node]:
                for ori in l_in[x_node][l]:
                    if ori not in visited:
                        neighbor[node].safe_add(ori, statics.fade_factor_pow[next_dep], target='in')
                        visited.add(ori)
                        if next_dep < statics.neighbor_threshold:
                            q_node.put(ori)
                            q_dep.put(next_dep)
        neighbor[node].cal_module(target='in')
    # 先不统计出度
    t_end_neighbor = time.clock()  # timer
    print("统计邻居信息耗时 " + str(t_end_neighbor - t_start_neighbor))
    print("统计邻居信息耗时 " + str(t_end_neighbor - t_start_neighbor), file=statics.f_cons)

    return l_in, l_out, l_in_menu, l_out_menu, node_set, neighbor


def __inner_sort(arr, menu):
    """
    将点对应标签的对应点按照从小到大顺序排序
    """
    for node in menu:
        menu[node].sort()
        for label in menu[node]:
            arr[node][label].sort()
