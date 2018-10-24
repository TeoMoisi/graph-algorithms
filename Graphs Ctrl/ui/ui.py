from ctrl.ctrl import Controller

class UI(object):

    ctrl = Controller()

    def __init__(self):
        '''

        '''
        self.ctrl = Controller()

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
        print("7: Press 7 in order to modify the information/the integer attached to a specified edge.")
        print("8: Press 8 in order to add a new vertex.")
        print("9: Press 9 to remove an existing vertex.")
        print("10: Press 10 to add a new edge between two vertices.")
        print("11: Press 11 to remove an existing edeg between 2 vertices.")
        print("12: Press 12 in order to print all the edges, outbound and inbound vertices.")

    def vertices(self):
        '''
        Function to print the number of the vertices
        :return: int
        '''
        print(len(self.ctrl.get_out()))

    def is_edge(self):
        x = input("1st vertex:")
        y = input("2nd vertex: ")
        if self.ctrl.is_edge(x, y):
            print("There is an edge from ", x, " to ", y)
        else:
            print("There isn't an edge from ", x, " to ", y)

    def in_degree(self):
        x = input("Please input the vertex: ")
        print("In degree: ", self.ctrl.get_in_degree(x))

    def out_degree(self):
        x = input("Please input the vertex: ")
        print("Out degree: ", self.ctrl.get_out_degree(x))


    def inbound(self):
        v = input("Please input the vertex: ")
        l = []
        for edge in self.ctrl.get_inbound_v(v):
            l.append(edge)
        if self.ctrl.get_inbound_v(v) != []:

            print("The inbound of the vertex", v, " is: ")
            for i in range(0, len(l)):
                print(l[i])
        else:
            print("The inbound of the vertex", v, " is empty")


    def outbound(self):
        v = input("Please input the vertex: ")
        l = []
        for edge in self.ctrl.get_outbound_v(v):
            l.append(edge)
        if self.ctrl.get_outbound_v(v) != []:

            print("The outbound of the vertex", v, " is: ")
            for i in range(0, len(l)):
                print(l[i])
        else:
            print("The outbound of the vertex", v, " is empty")

    def update_edge(self):
        v1 = input("Please input the first vertex: ")
        v2 = input("Please input the second vertex: ")
        c = input("Please input the cost: ")
        self.ctrl.update_the_edge(v1, v2, c)

    def add_vertex(self):
        vertex = input("Please input an integer positive number: ")
        self.ctrl.add_a_vertex(vertex)

    def remove_vertex(self):
        vertex = input("Please input an integer positive number: ")
        self.ctrl.remove_a_vertex(vertex)

    def add_edge(self):
        v1 = input("Please input the first vertex: ")
        v2 = input("Please input the second vertex: ")
        cost = input("Please input the value of the cost: ")
        self.ctrl.add_an_edge(v1, v2, cost)

    def remove_edge(self):
        v1 = input("Please input the first vertex: ")
        v2 = input("Please input the second vertex: ")
        self.ctrl.remove_an_edge(v1, v2)

    def print_all(self):
        print("Edges: ", self.ctrl.get_edges())
        print("Out: ", self.ctrl.get_out())
        print("In: ", self.ctrl.get_in())


    def menu(self):
        self.welcome()
        while True:
            self.print_menu()
            option = input("    Please input an option: ")
            if option == "0":
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
                    print("The new vertex has been successfully added! Now there are", len(self.ctrl.get_out()), "vertices." )
                except ValueError as error:
                    print(error)
                print("\n")
            elif option == "9":
                try:
                    self.remove_vertex()
                    print("The new vertex has been successfully removed! Now there are", len(self.ctrl.get_out()),
                          "vertices.")
                except ValueError as error:
                    print(error)
                print("\n")
            elif option == "10":
                try:
                    self.add_edge()
                except ValueError as error:
                    print(error)
                print("\n")
            elif option == "11":
                try:
                    self.remove_edge()
                except ValueError as error:
                    print(error)
                print("\n")
            elif option == "12":
                self.print_all()
            else:
                print("This option does not exits!\n")
