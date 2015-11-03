__author__ = 'alex'

class tree_node:
    def __init__(self, data=None):
        if data == None:
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
