from repo.repo import Repository
from validator.validator import Validator


class Controller(object):

    def __init__(self):
        '''
        Constructor for Controller class.
        '''
        self.__repo = Repository()
        self.__validator = Validator()

    def get_out(self):
        '''
        Returns the outbound dictionary.
        :return: outbound dictionary
        '''
        return self.__repo.get_out()

    def get_in(self):
        '''
        Returns the inbound dictionary.
        :return: inbound dictionary
        '''
        return self.__repo.get_in()

    def is_edge(self, x, y):
        '''
        This function checks whether the vertices x and y form an edge.
        :param x: integer
        :param y: integer
        :return: true if the vertices form an edge, false otherwise.
        '''
        self.__validator.is_integer(x)
        self.__validator.is_integer(y)
        self.__validator.valid_edge(x, y, self.get_out())
        return self.__repo.is_edge(int(x), int(y))

    def get_out_degree(self, v):
        '''
        Function which returns the out degree of a vertex.
        :param v: integer
        :return: integer
        '''

        self.__validator.is_integer(v)
        self.__validator.vertex_valid(v, self.get_out())
        return self.__repo.get_out_degree(int(v))

    def get_in_degree(self, v):
        '''
        Function which returns the in degree of a vertex.
        :param v: integer
        :return: integer
        '''
        self.__validator.is_integer(v)
        self.__validator.vertex_valid(v, self.get_in())
        return self.__repo.get_in_degree(int(v))

    def get_outbound_v(self, v):
        '''
        Function which returns the outbound of a veretx.
        :param v: ineteger
        :return: integer
        '''
        self.__validator.is_integer(v)
        self.__validator.vertex_valid(v, self.get_out())
        return self.__repo.get_outbound(int(v))

    def get_inbound_v(self, v):
        '''
        Function which rerturns the inbound of a vertex.
        :param v: integer
        :return: integer
        '''
        self.__validator.is_integer(v)
        self.__validator.vertex_valid(v, self.get_in())
        return self.__repo.get_inbound(int(v))

    def get_edges(self):
        '''
        Returns the edges dictionary.
        :return: edges dictionary
        '''
        return self.__repo.get_edges()

    def update_the_edge(self, v1, v2, c):
        '''
        This function updates an edge.
        :param v1: integer
        :param v2: integer
        :param c: integer
        :return:
        '''
        self.__validator.is_integer(v1)
        self.__validator.is_integer(v2)
        self.__validator.validate_cost(c)
        self.__validator.update_edge(int(v1), int(v2), int(c), self.get_edges())
        self.__repo.update_the_edge(int(v1), int(v2), int(c))

    def add_a_vertex(self, vertex):
        '''
        Function to add a vertex.
        :param vertex: integer
        :return:
        '''
        self.__validator.is_integer(vertex)
        self.__validator.valid_add_v(vertex, self.get_out())
        self.__repo.add_vertex(int(vertex))

    def remove_a_vertex(self, vertex):
        '''
        Function to remove a vertex.
        :param vertex: integer
        :return:
        '''
        self.__validator.is_integer(vertex)
        self.__validator.vertex_valid(vertex, self.get_out())
        self.__repo.remove_vertex(int(vertex))

    def add_an_edge(self, v1, v2, cost):
        '''
        Function to add an edge.
        :param v1: integer
        :param v2: integer
        :param cost: integer
        :return:
        '''
        self.__validator.is_integer(v1)
        self.__validator.is_integer(v2)
        self.__validator.validate_cost(cost)
        self.__validator.add_edge(int(v1), int(v2), self.get_edges())
        self.__repo.add_edge(int(v1), int(v2), int(cost))

    def remove_an_edge(self, v1, v2):
        '''
        Function to remove an edge.
        :param v1: integer
        :param v2: integer
        :return:
        '''
        self.__validator.is_integer(v1)
        self.__validator.is_integer(v2)
        self.__validator.valid_edge(v1, v2, self.get_out())
        self.__validator.remove_edge(int(v1), int(v2), self.get_edges())
        self.__repo.remove_edge(int(v1), int(v2))