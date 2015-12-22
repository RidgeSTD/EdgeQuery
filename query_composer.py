import time
import statics
from common import Twig
from common import DegreeTuple
from common import ROOT_PATH

__author__ = 'alex'


def compose_query(file_name=None):
    print("开始加载查询文件...")
    print("开始加载查询文件...", file=statics.f_cons)
    t1 = time.clock()

    if file_name is None:
        file_name = ROOT_PATH + "queries.txt"
    queries = []
    q_in = []
    q_out = []
    q_in_menu = []
    q_out_menu = []
    q_counter = -1

    q_file = open(file_name, 'r')
    has_more_query = True
    while has_more_query:
        queries.append([])
        q_in.append({})
        q_out.append({})
        flaged = set()
        degree = {}
        e_counter = 0
        while True:
            line = q_file.readline()
            if len(line) < 1:
                # 文件尾部
                q_counter += 1
                has_more_query = False
                break
            if len(line) == 1:
                # 两个查询之间的分割空行
                q_counter += 1
                break
            e_counter += 1
            line = line.split('\t')
            ori = int(line[0])
            edg = int(line[1])
            des = int(line[2])
            try:
                degree[ori].chg_out_degree(delt=1)
            except KeyError:
                degree[ori] = DegreeTuple(in_degree=0, out_degree=1)

            try:
                degree[des].chg_in_degree(delt=1)
            except KeyError:
                degree[des] = DegreeTuple(in_degree=1, out_degree=0)

            try:
                q_in[q_counter + 1][des].append((edg, ori))
            except KeyError:
                q_in[q_counter + 1][des] = []
                q_in[q_counter + 1][des].append((edg, ori))

            try:
                q_out[q_counter + 1][ori].append((edg, des))
            except KeyError:
                q_out[q_counter + 1][ori] = []
                q_out[q_counter + 1][ori].append((edg, des))

        t3 = time.clock()
        while e_counter > 0:
            head = __find_head(degree=degree, flaged=flaged)
            m_twig = Twig(head=head)
            m_twig.in_edge, m_twig.out_edge = __build_twig_prune_query(head=head, in_set=q_in[q_counter],
                                                                       out_set=q_out[q_counter],
                                                                       flaged=flaged, degree=degree)
            flaged.add(head)
            e_counter -= (len(m_twig.in_edge) + len(m_twig.out_edge))
            queries[q_counter].append(m_twig)
        t4 = time.clock()
        print('分割第' + str(len(queries)) + " 个查询耗时 " + str(t4 - t3))
        print('分割第' + str(len(queries)) + " 个查询耗时 " + str(t4 - t3), file=statics.f_cons)

        t5 = time.clock()
        q_in_menu.append({})
        for node in q_in[q_counter]:
            q_in_menu_counter = {}
            q_in_menu[q_counter][node] = []
            for label, ori in q_in[q_counter][node]:
                if label not in q_in_menu_counter:
                    q_in_menu_counter[label] = 1
                else:
                    q_in_menu_counter[label] += 1
                    # 这里与degree的统计信息重复了!
            for label in q_in_menu_counter:
                q_in_menu[q_counter][node].append((label, q_in_menu_counter[label]))
            q_in_menu[q_counter][node].sort(key=lambda x: x[0])

        q_out_menu.append({})
        for node in q_out[q_counter]:
            q_out_menu_counter = {}
            q_out_menu[q_counter][node] = []
            for label, ori in q_out[q_counter][node]:
                if label not in q_out_menu_counter:
                    q_out_menu_counter[label] = 1
                else:
                    q_out_menu_counter[label] += 1
                    # 这里与degree的统计信息重复了!
            for label in q_out_menu_counter:
                q_out_menu[q_counter][node].append((label, q_out_menu_counter[label]))
            q_out_menu[q_counter][node].sort(key=lambda x: x[0])
        t6 = time.clock()
        print("统计查询信息耗时 " + str(t6 - t5))
        print("统计查询信息耗时 " + str(t6 - t5), file=statics.f_cons)

        t2 = time.clock()
        print("加载查询共耗时 " + str(t2 - t1))
        print("加载查询共耗时 " + str(t2 - t1), file=statics.f_cons)

    q_file.close()

    return queries, q_in, q_out, q_in_menu, q_out_menu


def __find_head(degree, flaged):
    maxv = -9999
    maxp = None
    for node in degree:
        if node in flaged:
            continue
        tmp = degree[node].get_degree()
        if tmp > maxv:
            maxv = tmp
            maxp = node
    return maxp


def __build_twig_prune_query(head, in_set, out_set, degree, flaged):
    in_edge = []
    out_edge = []
    if head in in_set:
        for edg, ori in in_set[head]:
            if ori not in flaged:
                degree[ori].chg_out_degree(delt=-1)
                in_edge.append((edg, ori))
    if head in out_set:
        for edg, des in out_set[head]:
            if des not in flaged:
                degree[des].chg_in_degree(delt=-1)
                out_edge.append((edg, des))
    in_edge.sort(key=lambda x: x[0])
    out_edge.sort(key=lambda x: x[0])
    return in_edge, out_edge
