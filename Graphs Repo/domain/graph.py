class Graph(object):

    def __init__(self, n):
        """
        Constructor for class Graph.
        :param n: positive int
        """
        self.__in = {}
        self.__out = {}
        self.__edges = {}
        for i in range(0, n):
            self.__in[i] = []
            self.__out[i] = []

    def get_in(self):
        '''
        Returns the inbound dictionary.
        :return: inbound dictionary
        '''
        return self.__in

    def get_out(self):
        '''
        Returns the outbound dictionary.
        :return: outbound dictionary
        '''
        return self.__out

    def get_edge(self, x, y):
        return self.__edges[(x, y)]

    def get_edges(self):
        '''
        Returns the edges' dictionary.
        :return: edges' dictionary
        '''
        return self.__edges

    def add_vertex(self, vertex):
        '''
        Adds a vertex.
        :param vertex: integer
        :return:
        '''
        self.__in[vertex] = []
        self.__out[vertex] = []

    def add_edge(self, x, y, e):
        '''
        Adds an edge.
        :param x: integer
        :param y: integer
        :param e: integer
        :return:
        '''
        self.__out[x].append(y)
        self.__in[y].append(x)
        self.__edges[(x, y)] = e


    def is_edge(self, x, y):
        '''
        This function checks if an edge exists or not. It returns true if it exists and false otherwise
        :param x: integer
        :param y: integer
        :return: true/false
        '''
        if x in self.__in[y]:
            return True
        else:
            return False

    def set_edge(self, v1, v2, cost):
        '''
        This function updates an edge
        :param v1: integer
        :param v2: integer
        :param cost: integer
        :return:
        '''
        self.__edges[(v1, v2)] = cost


    def  remove_vertex(self, vertex):
        '''
        This function removes a vertex.
        :param vertex: integer
        :return:
        '''
        for i in self.__out:
            if (i, vertex) in self.__edges:
                self.__edges.pop((i, vertex))
            if (vertex, i) in self.__edges:
                self.__edges.pop((vertex, i))
            if vertex in self.__out[i]:
                (self.__out[i]).remove(vertex)
            if vertex in self.__in[i]:
                (self.__in[i]).remove(vertex)
        self.__out.pop(vertex)
        self.__in.pop(vertex)


    def remove_edge(self, v1, v2):
        """
        Removes an edge.
        :param x: int
        :param y: int
        :return: -
        """
        self.__edges.pop((v1, v2))
        self.__out[v1].remove(v2)
        self.__in[v2].remove(v1)
