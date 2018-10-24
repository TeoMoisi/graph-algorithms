import os

from domain.graph import Graph


class Repository(object):

    def __init__(self):
        '''
        Constructor for Repository class.
        '''
        self.__fileName = os.path.abspath("graph.txt")
        self.__graph = self.__loadFromFile()


    def __loadFromFile(self):
        '''
        Function to load the content of the file.
        :return: graph object
        '''
        f = open(self.__fileName, "r")
        line = f.readline().strip().split()
        graph = Graph(int(line[0]))
        for i in range(0, int(line[1])):
            line = f.readline().strip().split()
            graph.add_edge(int(line[0]), int(line[1]), int(line[2]))
        f.close()
        return graph

    def __storeToFile(self):
        '''
        Function to store information to file.
        :return:
        '''
        f = open(self.__fileName, "w")
        edges = self.__graph.get_edges()
        out = self.__graph.get_out()
        nr_vertices = len(self.__graph.get_out())
        nr_edges = len(edges)
        f.write(str(nr_vertices) + " " + str(nr_edges) + "\n")
        for i in out:
            if out[i]!=[]:
                for j in out[i]:
                    string_e = str(i) + " " + str(j) + " " + str(edges[(i, j)]) + "\n"
                    f.write(string_e)

    def get_out(self):
        '''
        Returns the outbound dictionary.
        :return: outbound dictionary
        '''
        return self.__graph.get_out()

    def get_in(self):
        '''
        Returns the inbound dictionary.
        :return: inbound dictionary
        '''
        return self.__graph.get_in()

    def get_edges(self):
        '''
        Returns the edges dictionary.
        :return: edges dictionary
        '''
        return self.__graph.get_edges()


    def is_edge(self, x, y):
        '''
        This function checks whether x and y, which are vertices, form an edge or not.
        :param x: integer
        :param y: integer
        :return: True/False
        '''
        return self.__graph.is_edge(x, y)


    def get_inbound(self, x):
        '''
        Returns a list of the intbound of a vertex.
        :param x: integer
        :return: list
        '''
        return self.__graph.get_in()[x]

    def get_outbound(self, x):
        '''
        Returns a list of the outbound of a vertex.
        :param x: integer
        :return: list
        '''
        return self.__graph.get_out()[x]


    def get_out_degree(self, x):
        '''
        Returns the out degree of a vertex.
        :param x: integer
        :return: integer
        '''
        return len(self.get_outbound(x))

    def get_in_degree(self, x):
        '''
        Returns the in degree of a vertex.
        :param x: integer.
        :return: integer.
        '''
        return len(self.get_inbound(x))

    def add_edge(self, x, y, c):
        '''
        Adds an edge.
        :param x: integer
        :param y: integer
        :param c: integer
        :return:
        '''
        self.__graph.add_edge(x, y, c)
        self.__storeToFile()

    def add_vertex(self, x):
        '''
        Adds a vertex.
        :param x: integer
        :return:
        '''
        self.__graph.add_vertex(x)
        #self.__storeToFile()

    def update_the_edge(self, v1, v2, cost):
        '''
        Updates an edge.
        :param v1: integer
        :param v2: integer
        :param cost: integer
        :return:
        '''
        self.__graph.set_edge(v1, v2, cost)
        self.__storeToFile()

    def remove_vertex(self, vertex):
        '''
        Removes a vertex.
        :param vertex: integer
        :return:
        '''
        self.__graph.remove_vertex(vertex)
        self.__storeToFile()

    def add_edge(self, v1, v2, c):
        '''
        Adds an edge.
        :param v1: integer
        :param v2: integer
        :param c: integer
        :return:
        '''
        self.__graph.add_edge(v1, v2, c)
        self.__storeToFile()

    def remove_edge(self, v1, v2):
        '''
        Removes an edge.
        :param v1: integer
        :param v2: integer
        :return:
        '''
        self.__graph.remove_edge(v1, v2)
        self.__storeToFile()

