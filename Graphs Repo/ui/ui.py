from repo.repo import Repository
from validator.validator import Validator
from domain.graph import Graph
import os

class UI(object):

    repo = Repository()
    validator = Validator()

    def __init__(self):
        '''

        '''
        self.repo = Repository()
        self.validator = Validator()
        self.__fileName = os.path.abspath("graph.txt")
        self.__fileNameSaved = os.path.abspath("saved")
        self.graph = self.__loadFromFile()


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

    @staticmethod
    def welcome():
        print("    Welcome to the graph application! These are the following options: ")


    @staticmethod
    def print_menu():
        print("0: Press 0 to exit the programme.")
        print("1: Press 1 to get the number of the vertices.")
        print("2: Press 2 in order to find whether there is an edge between 2 given vertices.")
        print("3: Press 3 to find the in degree of a vertex.")
        print("4: Press 4 to find the out degree of a vertex.")
        print("5: Press 5 to get the inbound edges of a vertex")
        print("6: Press 6 to get the outbound edges of a vertex")
        print("7: Press 7 in order to retrieve or modify the information/the integer attached to a specified edge.")
        print("8: Press 8 in order to add a new vertex.")
        print("9: Press 9 to remove an existing vertex.")
        print("10: Press 10 to add a new edge between two vertices.")
        print("11: Press 11 to remove an existing edge between 2 vertices.")
        print("12: Press 12 in order to print all the edges, outbound and inbound vertices.")
        print("13: Press 13 in order to retrieve the information of an edge.")

    def vertices(self):
        '''
        Function to print the number of the vertices
        :return: int
        '''
        print(len(self.graph.get_out()))

    def is_edge(self):
        x = input("1st vertex:")
        y = input("2nd vertex: ")
        self.validator.is_integer(x)
        self.validator.is_integer(y)
        self.validator.valid_edge(x, y, self.repo.get_out())
        if self.repo.is_edge(int(x), int(y)):
            print("There is an edge from ", x, " to ", y)
        else:
            print("There isn't an edge from ", x, " to ", y)

    def in_degree(self):
        x = input("Please input the vertex: ")
        self.validator.is_integer(x)
        self.validator.vertex_valid(x, self.repo.get_in())
        print("In degree: ", self.repo.get_in_degree(int(x)))

    def out_degree(self):
        x = input("Please input the vertex: ")
        self.validator.is_integer(x)
        self.validator.vertex_valid(x, self.repo.get_out())
        print("Out degree: ", self.repo.get_out_degree(int(x)))


    def inbound(self):
        v = input("Please input the vertex: ")
        l = []
        self.validator.is_integer(v)
        self.validator.vertex_valid(v, self.repo.get_in())
        for edge in self.repo.get_inbound(int(v)):
            l.append(edge)
        if self.repo.get_inbound(int(v)) != []:

            print("The inbound of the vertex", v, " is: ")
            for i in range(0, len(l)):
                print(l[i])
        else:
            print("The inbound of the vertex", v, " is empty")


    def outbound(self):
        v = input("Please input the vertex: ")
        l = []
        self.validator.is_integer(v)
        self.validator.vertex_valid(v, self.repo.get_out())
        for edge in self.repo.get_outbound(int(v)):
            l.append(edge)
        if self.repo.get_outbound(int(v)) != []:

            print("The outbound of the vertex", v, " is: ")
            for i in range(0, len(l)):
                print(l[i])
        else:
            print("The outbound of the vertex", v, " is empty")

    def update_edge(self):
        v1 = input("Please input the first vertex: ")
        v2 = input("Please input the second vertex: ")
        c = input("Please input the cost: ")
        self.validator.is_integer(v1)
        self.validator.is_integer(v2)
        self.validator.validate_cost(c)
        self.validator.update_edge(int(v1), int(v2), int(c), self.repo.get_edges())
        self.repo.update_the_edge(int(v1), int(v2), int(c))

    def add_vertex(self):
        vertex = input("Please input an integer positive number: ")
        self.validator.is_integer(vertex)
        self.validator.valid_add_v(vertex, self.repo.get_out())
        self.repo.add_vertex(int(vertex))

    def remove_vertex(self):
        vertex = input("Please input an integer positive number: ")
        self.validator.is_integer(vertex)
        self.validator.vertex_valid(vertex, self.repo.get_out())
        self.repo.remove_vertex(int(vertex))

    def add_edge(self):
        v1 = input("Please input the first vertex: ")
        v2 = input("Please input the second vertex: ")
        cost = input("Please input the value of the cost: ")
        self.validator.is_integer(v1)
        self.validator.is_integer(v2)
        self.validator.validate_cost(cost)
        self.validator.add_edge(int(v1), int(v2), self.repo.get_edges())
        self.repo.add_edge(int(v1), int(v2), int(cost))

    def remove_edge(self):
        v1 = input("Please input the first vertex: ")
        v2 = input("Please input the second vertex: ")
        self.validator.is_integer(v1)
        self.validator.is_integer(v2)
        self.validator.valid_edge(v1, v2, self.repo.get_out())
        self.validator.remove_edge(int(v1), int(v2), self.repo.get_edges())
        self.repo.remove_edge(int(v1), int(v2))

    def print_all(self):
        print("Edges: ", self.repo.get_edges())
        print("Out: ", self.repo.get_out())
        print("In: ", self.repo.get_in())

    def retrieve(self):
        v1 = input("Please input the first vertex: ")
        v2 = input("Please input the second vertex: ")
        self.validator.is_integer(v1)
        self.validator.is_integer(v2)
        if self.repo.is_edge(int(v1), int(v2)):
            return self.repo.get_edge(int(v1), int(v2))

    def __storeToFile(self):
        '''
        Function to store information to file.
        :return:
        '''
        f = open(self.__fileNameSaved, "w")
        edges = self.repo.get_edges()
        out = self.repo.get_out()
        nr_vertices = len(self.repo.get_out())
        nr_edges = len(edges)
        f.write(str(nr_vertices) + " " + str(nr_edges) + "\n")
        for i in out:
            if out[i]!=[]:
                for j in out[i]:
                    string_e = str(i) + " " + str(j) + " " + str(edges[(i, j)]) + "\n"
                    f.write(string_e)
            else:
                string_e = str(i) + "  " + "  " + "\n"
                f.write(string_e)

    def save(self):
        self.__storeToFile()


    def menu(self):
        self.welcome()
        while True:
            self.print_menu()
            option = input("    Please input an option: ")
            if option == "0":
                sub_op = input("Do you want to save the modifications? ")
                if sub_op == "yes":
                    self.save()
                    print("The modifications were saved in saved.txt file.\n")
                else:
                    break
            elif option == "1":
                self.vertices()
                print("\n")
            elif option == "2":
                try:
                    self.is_edge()
                except ValueError as error:
                    print(error)
                print("\n")
            elif option == "3":
                try:
                    self.in_degree()
                except ValueError as error:
                    print(error)
                print("\n")
            elif option == "4":
                try:
                    self.out_degree()
                except ValueError as error:
                    print(error)
                print("\n")
            elif option == "5":
                try:
                    self.inbound()
                except ValueError as error:
                    print(error)
                print("\n")
            elif option == "6":
                try:
                    self.outbound()
                except ValueError as error:
                    print(error)
                print("\n")
            elif option == "7":
                try:
                    self.update_edge()
                    print("The edge has been successfully updated!")
                except ValueError as error:
                    print(error)
                print("\n")
            elif option == "8":
                try:
                    self.add_vertex()
                    print("The new vertex has been successfully added! Now there are", len(self.repo.get_out()), "vertices." )
                except ValueError as error:
                    print(error)
                print("\n")
            elif option == "9":
                try:
                    self.remove_vertex()
                    print("The new vertex has been successfully removed! Now there are", len(self.repo.get_out()),
                          "vertices.")
                except ValueError as error:
                    print(error)
                print("\n")
            elif option == "10":
                try:
                    self.add_edge()
                    print("The edge was successfully added!\n")
                except ValueError as error:
                    print(error)
                print("\n")
            elif option == "11":
                try:
                    self.remove_edge()
                    print("The edge was successfully removed!\n")
                except ValueError as error:
                    print(error)
                print("\n")
            elif option == "12":
                self.print_all()
            elif option == "13":
                try:
                    print("The cost is: ", self.retrieve())
                except ValueError as error:
                    print(error)
                print("\n")
            else:
                print("This option does not exits!\n")
