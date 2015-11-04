__author__ = 'alex'


from common import Twig
from common import DegreeTuple


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


def compose_query(file_name=None):
    if file_name is None:
        file_name = "/Users/alex/queries.txt"
    queries = []
    q_counter = -1

    q_file = open(file_name, 'r')
    has_more_query = True
    while has_more_query:
        queries.append([])
        in_set = {}
        out_set = {}
        flaged = set()
        degree = {}
        e_counter = 0
        while True:
            line = q_file.readline()
            if len(line) < 1:
                # 文件尾部
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
                in_set[des].append((edg, ori))
            except KeyError:
                in_set[des] = []
                in_set[des].append((edg, ori))

            try:
                out_set[ori].append((edg, des))
            except KeyError:
                out_set[ori] = []
                out_set[ori].append((edg, des))

        while e_counter > 0:
            head = __find_head(degree=degree, flaged=flaged)
            m_twig = Twig(head=head)
            m_twig.in_edge, m_twig.out_edge = __build_twig_prune_query(head=head, in_set=in_set, out_set=out_set, flaged=flaged, degree=degree)
            flaged.add(head)
            e_counter -= (len(m_twig.in_edge) + len(m_twig.out_edge))
            queries[q_counter].append(m_twig)

    return queries
