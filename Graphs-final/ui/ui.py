from validator.validator import Validator
from domain.graph import Graph
import os
import math
from copy import deepcopy
import queue


class UI(object):

    validator = Validator()

    def __init__(self):
        '''
        Constructor fos UI class.
        '''
        self.validator = Validator()
        self.__fileName = os.path.abspath("small")
        self.__fileNameSaved = os.path.abspath("saved")
        self.__fileNameCopy = os.path.abspath("copy")
        self.graph = self.__loadFromFile()
        self.stack = []
        self.component = []
        self.expl = {}
        self.str_conn = []
        self.lists = []
        self.lengths = []

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
            #graph.add_edge(int(line[1]), int(line[0]), int(line[2]))
        f.close()
        return graph


    def maximal_clique(self, r, p, x):
        #bron kerbosch recursive alhorithm
        '''

        :param r: empty list
        :param p: all vertices
        :param x: empty list
        :return: all maximal cliques
        '''

        if (len(p) == 0) and (len(x) == 0):
            #when a maximal clique is found, it is added into a list
            self.lists.append(r)
            self.lengths.append(len(r))

        for vertex in p[:]:
            potential_clique_new = r[:]
            #adding the veretx to the potential_clique list
            potential_clique_new.append(vertex)
            #a list with all the neighbours of the vertex
            neighbour = self.get_outbound(vertex)
            #p_new = p intersected with neighbour
            p_new = [val for val in p if val in neighbour]
            #x_new = x intersected with neighbour
            x_new = [val for val in x if val in neighbour]
            #recursive step
            self.maximal_clique(potential_clique_new, p_new, x_new)

            p.remove(vertex)
            x.append(vertex)



    def DAG(self):
        '''
        Method to perform the topologial sorting of the activities
        :return: the topological sorted list of activities or None if the graph isn't a DAG
        '''
        sorted = []
        queue = []
        count = {}
        for node in self.graph.get_vertices():
            count[node] = len(self.get_inbound(node))
            #if node has no predecesors, we put the node in the queue
            if count[node] == 0:
                queue.append(node)

        while queue:
            #while the queue is not empty
            node = queue.pop(-1)
            sorted.append(node)
            for y in self.get_outbound(node):
                count[y] = count[y] - 1
                if count[y] == 0:
                    queue.append(y)

        #if the final sorted list does not contain all the verices from the graph, it isn't a DAG
        if len(sorted) < len(self.graph.get_vertices()):
            sorted = None

        return sorted


    def starting_times(self, duration):
        '''
        Method to find the earliest and the latest starting time for each activity
        :param duration: a list durations for each activity
        :return: a tuple of lists representing the earliest and the latest starting time
        '''
        topoSort = self.DAG()
        early = [0] * len(topoSort)

        #performing the earliest starting time
        for i in topoSort:
            t_max = 0
            for j in self.get_inbound(i):
                t_max = max(t_max, early[j] + duration[j])
            early[i] = t_max


        late = [0] * len(topoSort)
        late[topoSort[-1]] = early[topoSort[-1]]
        topoSort.reverse()

        #performing the latest starting time
        for i in topoSort:
            if i == topoSort[0]:
                continue
            t_min = math.inf
            for j in self.get_outbound(i):
                t_min = min(t_min, late[j] - duration[i])
            late[i] = t_min

        #if the earliest and the latest starting time are equal, then the corresponding activity is critical
        for i in topoSort:
            if early[i] == late[i]:
                print(i, "is a critical activity.")

        #printing the total time of the project
        print("The total time of the project is: ", early[topoSort[0]] + duration[topoSort[0]])
        return (early, late)



    def bellman(self, source, target):
        previous = {}
        distance = {}
        queue = []
        visited = {}
        count = {}

        cost_dict = self.graph.get_edges()

        #we initialize the dictionaries
        for node in self.graph.get_vertices():
            distance[node] = math.inf
            previous[node] = None
            count[node] = 0
            #no node is visited at the beginning
            visited[node] = False

        #the distance is 0 at the beginning
        distance[source] = 0

        #push the source in the queue
        queue.append(source)

        #the source vertex is marked as visited
        visited[source] = True

        #while the queue is not empty
        while queue:
            vertex = queue[0]
            queue.pop(0)
            visited[vertex] = False #the vertex is marked as not visited
            for child in self.get_outbound(vertex): #search through all its neoghbours
                if distance[child] > distance[vertex] + cost_dict[(vertex, child)]:
                    distance[child] = distance[vertex] + cost_dict[(vertex, child)] #update the distance
                    previous[child] = vertex

                    if visited[child] == False:
                        visited[child] = True #child is marked as true
                        count[child] += 1
                        queue.append(child) #push the child in the queue

                        #if the number of vertices is greater than the maximum number of vertices, we have negative cost cycle
                        if count[child] >= len(self.graph.get_out()):
                            print("Negative cost cycle!")
                            return None

        #returns a pair distance, path
        msg = "no path"
        if distance[target] == math.inf:
            print("no path")
            return msg
        return (distance[target], self.get_path(source, target, previous))

    def get_path(self, v1, v2, dict):
        lista = []
        node = v2
        while node != v1:
            lista.append(node)
            node = dict[node]
        lista.append(v1)

        lista.reverse()
        return lista


    def dfs1(self, vertex):
        self.expl[vertex] = True
        for child in self.get_outbound(vertex):
            if self.expl[child] == False:
                self.dfs1(child)

        self.stack.append(vertex)

    def dfs2(self, vertex):
        self.expl[vertex] = True
        for child in self.get_inbound(vertex):
            if self.expl[child] == False:
                self.dfs2(child)

        self.component.append(vertex)
        print(self.component)

    def str_conected(self):
        ''' Kosaraju's algorithm for strongly connected components'''

        #all the vertices in the graph are marked as not visited/explored
        for vertex in self.graph.get_vertices():
            self.expl[vertex] = False

        for vertex in self.graph.get_vertices():
            if self.expl[vertex] == False:
                self.dfs1(vertex)

        for vertex in self.graph.get_vertices():
            self.expl[vertex] = False

        while self.stack:
            #build the strongly connected components
            vertex = self.stack[-1]
            if self.expl[vertex] == False:
                self.component.clear()
                self.dfs2(vertex)
                self.str_conn.append(deepcopy(self.component))

            self.stack.pop(-1)

        i = 1
        #printing the strongly connected components
        for comp in self.str_conn:
            comp.sort()
            print("component: ", i)
            print(comp)
            for v1 in comp:
                for v2 in comp:
                    if v1 != v2:
                        try:
                            #printing the edges in a strongly connected component
                            self.validator.valid_edge(v1, v2, self.graph.get_out())
                            print("edge: ", v1, "->", v2)
                        except ValueError as ve:
                            continue
            i += 1

        self.str_conn.clear()
        self.expl.clear()
        self.stack.clear()

    def bfs_shortest_path(self, start, goal):
        explored = [] #contains all the explored nodes
        #all the paths to be checked
        queue = [[start]] #contains all the checked paths

        # returns the path if start is goal
        if start == goal:
            msg = "Start = goal"
            return msg

        # keeps looping until all possible paths have been checked
        while queue:
            path = queue.pop(0) #pop the first path from the queue
            node = path[-1] #get the last node from the path
            if node not in explored:
                neighbours = self.get_outbound(node) # go through all neighbour nodes,
                # construct a new path and push it into the queue
                for neighbour in neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)
                    # return path if neighbour is goal
                    if neighbour == goal:
                        return new_path

                # mark node as explored
                explored.append(node)

        # in case there's no path between the 2 nodes
        msg = "The path doesn't exist!"
        return msg

    def bfs(self):
        start = input("Please input the first vertex: ")
        end = input("Please input the second vertex: ")
        self.validator.is_integer(start) #validates the input for the first veretx
        self.validator.is_integer(end) #validates the input for the second vertex
        l = self.bfs_shortest_path(int(start), int(end))
        print("The path is: ", l) #prints the list
        if (l != "The path doesn't exist!" and l != "That was easy! Start = goal"):
            print("The length is: ", len(l) - 1)

    @staticmethod
    def welcome():
        print("    Welcome to the graph application! "
              "These are the following options: ")


    @staticmethod
    def print_menu():
        print("0: Press 0 to exit the programme.")
        print("1: Press 1 to get the number of the vertices.")
        print("2: Press 2 in order to find whether there is an "
              "edge between 2 given vertices.")
        print("3: Press 3 to find the in degree of a vertex.")
        print("4: Press 4 to find the out degree of a vertex.")
        print("5: Press 5 to get the inbound edges of a vertex")
        print("6: Press 6 to get the outbound edges of a vertex")
        print("7: Press 7 in order to modify the information/the integer "
              "attached to a specified edge.")
        print("8: Press 8 in order to add a new vertex.")
        print("9: Press 9 to remove an existing vertex.")
        print("10: Press 10 to add a new edge between two vertices.")
        print("11: Press 11 to remove an existing edge between 2 vertices.")
        print("12: Press 12 in order to print all the edges, "
              "outbound and inbound vertices.")
        print("13: Press 13 in order to retrieve the information of an edge.")
        print("14. Press 14 for bfs.")
        print("15. Press 15 for strongly connectred components.")
        print("16. Bellman ")
        print("17. DAG & topological sorting.")
        print("18. Earliest and latest starting time/total duration/critical activities.")
        print("19. Return the maximal clique.")

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
        #self.validator.valid_edge(x, y, self.graph.get_out())
        if self.graph.is_edge(int(x), int(y)):
            print("There is an edge from ", x, " to ", y)
        else:
            print("There isn't an edge from ", x, " to ", y)


    def get_inbound(self, x):
        '''
        Returns a list of the intbound of a vertex.
        :param x: integer
        :return: list
        '''
        return self.graph.get_in()[x]

    def get_outbound(self, x):
        '''
        Returns a list of the outbound of a vertex.
        :param x: integer
        :return: list
        '''
        return self.graph.get_out()[x]

    def in_degree(self):
        x = input("Please input the vertex: ")
        self.validator.is_integer(x)
        self.validator.vertex_valid(x, self.graph.get_in())
        print("In degree: ", len(self.get_inbound(int(x))))

    def out_degree(self):
        x = input("Please input the vertex: ")
        self.validator.is_integer(x)
        self.validator.vertex_valid(x, self.graph.get_out())
        print("Out degree: ", len(self.get_outbound(int(x))))


    def inbound(self):
        v = input("Please input the vertex: ")
        l = []
        self.validator.is_integer(v)
        self.validator.vertex_valid(v, self.graph.get_in())
        for edge in self.get_inbound(int(v)):
            l.append(edge)
        if self.get_inbound(int(v)) != []:

            print("The inbound of the vertex", v, " is: ")
            for i in range(0, len(l)):
                print(l[i])
        else:
            print("The inbound of the vertex", v, " is empty")


    def outbound(self):
        v = input("Please input the vertex: ")
        l = []
        self.validator.is_integer(v)
        self.validator.vertex_valid(v, self.graph.get_out())
        for edge in self.get_outbound(int(v)):
            l.append(edge)
        if self.get_outbound(int(v)) != []:

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
        self.validator.update_edge(int(v1), int(v2), int(c), self.graph.get_edges())
        self.graph.set_edge(int(v1), int(v2), int(c))

    def add_vertex(self):
        vertex = input("Please input an integer positive number: ")
        self.validator.is_integer(vertex)
        self.validator.valid_add_v(vertex, self.graph.get_out())
        self.graph.add_vertex(int(vertex))

    def remove_vertex(self):
        vertex = input("Please input an integer positive number: ")
        self.validator.is_integer(vertex)
        self.validator.vertex_valid(vertex, self.graph.get_out())
        self.graph.remove_vertex(int(vertex))

    def add_edge(self):
        v1 = input("Please input the first vertex: ")
        v2 = input("Please input the second vertex: ")
        cost = input("Please input the value of the cost: ")
        self.validator.is_integer(v1)
        self.validator.is_integer(v2)
        self.validator.validate_cost(cost)
        self.validator.add_edge(int(v1), int(v2), self.graph.get_edges())
        self.graph.add_edge(int(v1), int(v2), int(cost))
        #self.graph.add_edge(int(v2), int(v1), int(cost))

    def remove_edge(self):
        v1 = input("Please input the first vertex: ")
        v2 = input("Please input the second vertex: ")
        self.validator.is_integer(v1)
        self.validator.is_integer(v2)
        self.validator.valid_edge(v1, v2, self.graph.get_out())
        self.validator.remove_edge(int(v1), int(v2), self.graph.get_edges())
        self.graph.remove_edge(int(v1), int(v2))

    def print_all(self):
        print("Edges: ", self.graph.get_edges())
        print("Out: ", self.graph.get_out())
        print("In: ", self.graph.get_in())

        for vert in self.graph.get_vertices():
            for child in self.get_outbound(vert):
                print(vert, child)

    def retrieve(self):
        v1 = input("Please input the first vertex: ")
        v2 = input("Please input the second vertex: ")
        self.validator.is_integer(v1)
        self.validator.is_integer(v2)
        if self.graph.is_edge(int(v1), int(v2)):
            return self.graph.get_edge(int(v1), int(v2))

    def __storeToFile(self):
        '''
        Function to save the modified graph to a new file.
        :return:
        '''
        f = open(self.__fileNameSaved, "w")
        edges = self.graph.get_edges()
        out = self.graph.get_out()
        inb = self.graph.get_in()
        nr_of_vertices = len(self.graph.get_out())
        nr_of_edges = len(edges)
        f.write(str(nr_of_vertices) + " " + str(nr_of_edges) + "\n")
        for i in out:
            if out[i]!=[]:
                for j in out[i]:
                    line = str(i) + " " + str(j) + " " + str(edges[(i, j)]) + "\n"
                    f.write(line)
            else:
                if inb[i] == []:
                    if out[i] == []:
                        line = str(i) + "  " + "  " + "\n"
                        f.write(line)

    def makeCopy(self):
        '''
        Function to make a copy of the file.
        :return:
        '''
        f = open(self.__fileNameCopy, "w")
        edges = self.graph.get_edges()
        out = self.graph.get_out()
        nr_vertices = len(self.graph.get_out())
        nr_edges = len(edges)
        f.write(str(nr_vertices) + " " + str(nr_edges) + "\n")
        for i in out:
            if out[i]!=[]:
                for j in out[i]:
                    string_e = str(i) + " " + str(j) + " " + str(edges[(i, j)]) + "\n"
                    f.write(string_e)


    def menu(self):
        self.makeCopy()
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
                    print("The new vertex has been successfully added! Now there are",
                          len(self.graph.get_out()), "vertices." )
                except ValueError as error:
                    print(error)
                print("\n")
            elif option == "9":
                try:
                    self.remove_vertex()
                    print("The new vertex has been successfully removed! Now there are",
                          len(self.graph.get_out()),
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
            elif option == "14":
                try:
                    self.bfs()
                except ValueError as error:
                    print(error)
                print("\n")
            elif option == "save":
                self.__storeToFile()
                print("The modifications were saved in saved.txt file.\n")
            elif option == "15":
                self.str_conected()
            elif option == "16":
                source = int(input("Please input the source: "))
                target = int(input("Please input the target: "))
                ret = self.bellman(source, target)
                if ret != None:
                    print("The distance is: ", ret[0])
                    print("The path is: ", ret[1])
            elif option == "17":
                sorted = self.DAG()
                print(sorted)
            elif option == "18":
                f = open("duration.txt", "r")
                nr = int(f.readline())
                duration = []
                for i in range(0, nr):
                    d = int(f.readline())
                    duration.append(d)
                f.close()
                (early, late) = self.starting_times(duration)
                for i in range(0, len(early)):
                    print("The earliest starting time for activity ", i, "is: ", early[i], " and the latest: ", late[i])
                #print(self.starting_times(duration))

            elif option == "19":
                p = []
                for i in self.graph.get_vertices():
                    p.append(i)
                r = []
                x = []
                self.maximal_clique(r, p, x)
                self.lengths.sort()
                for l in self.lists:
                    if len(l) == self.lengths[-1]:
                        print("The clique of maximum size is:", l)
                for l in self.lists:
                    if len(l) != self.lengths[-1]:
                        print("Maximal clique: ", l)
            else:
                print("This option does not exits!\n")
