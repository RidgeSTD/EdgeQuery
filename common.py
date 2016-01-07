import math

import statics
from data_structure_util import CQueue

__author__ = 'alex'


INVALID_CANDIDATE = -999
VALID_CANDIDATE = 0

ROOT_PATH = '/Users/alex/Workspace/2015-11/EdgeQuery/data/'


# ================   methods   =============


def intersect(a, b):
    """
    删
    This is much much slower than the builtin set.intersection!
    <s>
    Given two sorted list, return the intersection of them.

    *Each list shouldn't have duplicated data, according the attribute of set.*
    </s>
    """
    if len(a) == 0 or len(b) == 0:
        return []
    ha = 0
    hb = 0
    la = len(a) - 1  # limit of array a
    lb = len(b) - 1  # limit of array b
    tmp = CQueue()
    while True:
        p2 = __dimidiate_search_ge(a[ha], hb, lb, b)
        if p2 > lb:
            break
        if a[ha] == b[p2]:
            tmp.put(a[ha])
            ha += 1
            hb = p2 + 1
        else:
            ha += 1
            hb = p2

        if ha > la or hb > lb:
            break

        p1 = __dimidiate_search_ge(b[hb], ha, la, a)
        if p1 > la:
            break
        if a[p1] == b[hb]:
            tmp.put(b[hb])
            hb += 1
            ha = p1 + 1
        else:
            hb += 1
            ha = p1 + 1
        if ha > la or hb > lb:
            break
    return tmp.get_queue_copy()


def union(a, b):
    """
    删
    This is much much slower than the builtin set.union!
    <s>
    Given two sorted list, return the union of them.

    *Each list shouldn't have duplicated data, according the attribute of set.*
    </s>
    """
    if len(a) == 0:
        return b
    if len(b) == 0:
        return a
    ha = 0
    hb = 0
    la = len(a) - 1  # limit of array a
    lb = len(b) - 1  # limit of array b
    tmp = CQueue()
    while True:
        pb = __dimidiate_search_ge(a[ha], hb, lb, b)
        if pb < lb and a[ha] == b[pb]:
            tmp.extend(b[hb: pb + 1])
            ha += 1
            hb = pb + 1
        else:
            tmp.extend(b[hb: pb])
            tmp.put(a[ha])
            ha += 1
            hb = pb
        if ha > la or hb > lb:
            break

        pa = __dimidiate_search_ge(b[hb], ha, la, a)
        if pa < la and a[pa] == b[hb]:
            tmp.extend(a[ha: pa + 1])
            hb += 1
            ha = pa + 1
        else:
            tmp.extend(a[ha: pa])
            tmp.put(b[hb])
            hb += 1
            ha = pa
        if ha > la or hb > lb:
            break

    tmp.extend(a[ha: la + 1])
    tmp.extend(b[hb: lb + 1])

    return tmp.get_queue_copy()


def __dimidiate_search_ge(val, l, r, arr):
    """
    Search the given value *val* in sorted array *arr* with in search field from *l* to *r*

    Return the first postion *p* where the value is no less than *val*

    If there is no valid element return *r+1*

    """
    st = l - 1
    en = r + 1
    while st < en - 1:
        mid = math.floor((st + en)/2)
        if arr[mid] < val:
            st = mid
        else:
            en = mid
    return en


# ================   classes   =============


class TreeNode:
    def __init__(self, data=None):
        if data is None:
            data = []
        self.data = data
        self.children = {}
        self.label_menu = []
        self.prophesy = []

    def add_child(self, edge, c_node):
        statics.io_tree_node_count += 1  # TODO 调试!正式运行删除
        self.children[edge] = c_node
        self.label_menu.append(edge)

    def get_subtree_node_set(self):
        # 注：这里会不会非常非常慢啊！
        tmp = set(self.data)
        for edge in self.children:
            tmp = tmp.union(self.children[edge].get_subtree_node_set())
        return tmp


class Twig:
    def __init__(self, head=None):
        if head is None:
            raise ValueError
        self.head = head
        self.in_edge = []
        self.out_edge = []

    def add_in(self, label, node):
        self.in_edge.append((label, node))

    def add_out(self, label, node):
        self.out_edge.append((label, node))


class DegreeTuple:
    def __init__(self, in_degree=0, out_degree=0):
        self.__in_degree = in_degree
        self.__out_degree = out_degree
        self.__degree = in_degree + out_degree

    def get_in_degree(self):
        return self.__in_degree

    def get_out_degree(self):
        return self.__out_degree

    def get_degree(self):
        return self.__degree

    def set_in_degree(self, new_in_degree):
        self.__in_degree = new_in_degree
        self.__degree = self.__in_degree + self.__out_degree

    def chg_in_degree(self, delt):
        bak = self.__in_degree
        self.__in_degree += delt
        if self.__in_degree < 0:
            self.__in_degree = bak
            raise ValueError("in degree can not less then 0!")
        self.__degree += delt

    def set_out_degree(self, new_out_degree):
        self.__out_degree = new_out_degree
        self.__degree = self.__in_degree + self.__out_degree

    def chg_out_degree(self, delt):
        bak = self.__out_degree
        self.__out_degree += delt
        if self.__out_degree < 0:
            self.__out_degree = bak
            raise ValueError("out degree can not less then 0!")
        self.__degree += delt


class QueryBox:
    """
    :如果一个点不在candidate里, 意味着它与所有点产生映射!
    也就是 candidate[node]=None 与 candidate[node]={} 不一样!
    只有这个比较特殊!
    """
    def __init__(self, step):
        self.step = step
        self.candidate = {}

    def filter(self):
        """
        Filter all candidate by single projection
        if null set caused, return common.INVALIDATE_CANDIDAT
        :return:
        """
        pipe_line = CQueue()
        for node in self.candidate:
            if len(self.candidate[node]) == 1:
                griddle = None
                for each in self.candidate[node]:
                    griddle = each
                if griddle is None:
                    return INVALID_CANDIDATE
                for other in self.candidate:
                    if node != other:
                        try:
                            self.candidate[other].remove(griddle)
                            new_len = len(self.candidate[other])
                            if new_len < 1:
                                return INVALID_CANDIDATE
                            if new_len == 1:
                                pipe_line.put(other)
                        except:
                            pass

        while not pipe_line.is_empty():
            griddle = None
            x_node = pipe_line.get()
            for each in self.candidate[x_node]:
                griddle = each
            if griddle is None:
                return INVALID_CANDIDATE
            for other in self.candidate:
                if other != x_node:
                    try:
                        self.candidate[other].remove(griddle)
                        new_len = len(self.candidate[other])
                        if new_len < 1:
                            return INVALID_CANDIDATE
                        if new_len == 1:
                            pipe_line.put(other)
                    except:
                        pass

        return VALID_CANDIDATE

    def adapt_candidates(self, ex_candidates, filter_afterwards=True):
        for node in ex_candidates:
            if node in self.candidate:
                self.candidate[node] = self.candidate[node].intersection(ex_candidates[node])
            else:
                self.candidate[node] = ex_candidates[node]
        if filter_afterwards:
            return self.filter()
        return None


class NeighborInfo:
    """
    记录每个节点的邻居信息,包括in_nodes, in_nodes_menu, in_module, <s>out_nodes, out_nodes_label, out_module</s>
    """
    def __init__(self):
        self.in_nodes = {}
        self.in_nodes_menu = set()
        self.in_module = 0
        # self.out_nodes = {}
        # self.out_nodes_menu = set()
        # self.out_module = 0

    def safe_add(self, node, data, target='in'):
        if target == 'in':
            if node not in self.in_nodes_menu:
                self.in_nodes_menu.add(node)
                self.in_nodes[node] = data
            else:
                self.in_nodes[node] += data
        else:
            pass
            # if node in self.out_nodes_menu:
            #     self.out_nodes_menu.add(node)
            #     self.out_nodes[node] - data
            # else:
            #     self.out_nodes[node] += data

    def cal_module(self, target="in"):
        """
        -->计算点邻居信息得到的模

        target: 需要处理入度,传入'in', 反之传入'out'
        """
        tmp = 0
        if target == 'in':
            for node in self.in_nodes_menu:
                tmp += self.in_nodes[node] * self.in_nodes[node]
            self.in_module = math.sqrt(tmp)
        else:
            pass
