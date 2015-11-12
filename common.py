import statics

__author__ = 'alex'


INVALID_CANDIDATE = -999
VALID_CANDIDATE = 0


class TreeNode:
    def __init__(self, data=None):
        if data is None:
            data = []
        self.data = data
        self.children = {}
        self.label_menu = []

    def add_child(self, edge, c_node):
        self.children[edge] = c_node
        self.label_menu.append(edge)

    def traverse(self, debug=False):
        for edge in self.children:
            if debug:
                print(str(self.data) + " -" + str(edge) + "-> " + str(self.children[edge].data))
                print(str(self.data) + " -" + str(edge) + "-> " + str(self.children[edge].data), file=statics.f_cons)
            self.children[edge].traverse(debug)

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
        pipe_line = []
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
                                pipe_line.append(other)
                        except:
                            pass

        h = 0
        r = len(pipe_line)
        while h < r:
            griddle = None
            for each in self.candidate[pipe_line[h]]:
                griddle = each
            if griddle is None:
                return INVALID_CANDIDATE
            for other in self.candidate:
                if other != pipe_line[h]:
                    try:
                        self.candidate[other].remove(griddle)
                        new_len = len(self.candidate[other])
                        if new_len < 1:
                            return INVALID_CANDIDATE
                        if new_len == 1:
                            pipe_line.append(other)
                            r += 1
                    except:
                        pass

            h += 1

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
