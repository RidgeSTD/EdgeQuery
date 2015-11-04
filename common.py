__author__ = 'alex'


class TreeNode:
    def __init__(self, data=None):
        if data is None:
            data = []
        self.data = data
        self.children = {}

    def add_child(self, edge, c_node):
        self.children[edge] = c_node

    def traverse(self, debug=False):
        for edge in self.children:
            if debug:
                print(str(self.data) + " -" + str(edge) + "-> " + str(self.children[edge].data))
            self.children[edge].traverse(debug)


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
