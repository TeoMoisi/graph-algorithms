class Graph():

    def __init__(self, n):
        """
        Constructor for class Graph.
        :param n: an integer positive number
        """
        self.__in = {}
        self.__out = {}
        self.__edges = {}
        for i in range(0, n):
            self.__in[i] = []
            self.__out[i] = []

    def get_in(self):
        '''
        Method to return the inbound
        dictionary.
        :return: inbound dictionary
        '''
        return self.__in

    def get_out(self):
        '''
        Method to return the outbound
        dictionary.
        :return: outbound dictionary
        '''
        return self.__out

    def get_edges(self):
        '''
        Method to return the edges'
        dictionary.
        :return: edges' dictionary
        '''
        return self.__edges

    def add_vertex(self, vertex):
        '''
        Method to add a vertex.
        :param vertex: positive integer
        :return:
        '''
        self.__in[vertex] = []
        self.__out[vertex] = []

    def add_edge(self, x, y, e):
        '''
        method to add an edge.
        :param x: positive integer
        :param y: positive integer
        :param e: integer
        :return:
        '''
        self.__out[x].append(y)
        self.__in[y].append(x)
        self.__edges[(x, y)] = e


    def is_edge(self, x, y):
        '''
        This function checks if an edge
        exists or not. It returns true if it
        exists and false otherwise
        :param x: positive integer
        :param y: positive integer
        :return: true/false
        '''
        if x in self.__in[y]:
            return True
        else:
            return False

    def set_edge(self, v1, v2, cost):
        '''
        Method to update an edge.
        :param v1: positive integer
        :param v2: positive integer
        :param cost: integer
        :return:
        '''
        self.__edges[(v1, v2)] = cost


    def  remove_vertex(self, vertex):
        '''
        Method to remove a vertex.
        :param vertex: positive integer
        :return:
        '''
        for i in self.__out:
            if (vertex, i) in self.__edges:
                self.__edges.pop((vertex, i))
            if (i, vertex) in self.__edges:
                self.__edges.pop((i, vertex))
            if vertex in self.__in[i]:
                (self.__in[i]).remove(vertex)
            if vertex in self.__out[i]:
                (self.__out[i]).remove(vertex)

        self.__in.pop(vertex)
        self.__out.pop(vertex)


    def remove_edge(self, v1, v2):
        """
        Method to remove an edge.
        :param x: positive integer
        :param y: positive integer
        :return: -
        """
        self.__edges.pop((v1, v2))
        self.__out[v1].remove(v2)
        self.__in[v2].remove(v1)
