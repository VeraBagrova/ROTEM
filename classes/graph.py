from classes.node import Node
from classes.generateNode import GenerateNode
from classes.charge import Charge
from classes.heap import Heap
from collections import defaultdict

'''
 Храним граф как список смежности https://www.techiedelight.com/ru/graph-implementation-python/
 Но вместо индекса родительской вершины в листе, кладем каждого родителя в ключ словаря

 defaultdict, и словарь имеют одинаковую функциональность, за исключением того, что 
 defaultdict никогда не вызывает никаких KeyError, поскольку он предоставляет значение по умолчанию для ключа, 
 которого нет в словаре, созданном пользователем.
 defaultdict(list) - для любого ключа всегда есть пустой список

 для каждого ключа список списков [destination, weight]
'''


class Graph:

    # метод, генерирующий полный граф из нулевой вершины
    @classmethod
    def create_from_node(cls, node: Node, generator: GenerateNode, charge: Charge):
        all_nodes = [node]
        graph = defaultdict(list)
        list_nodes = [node]  # на каждом шаге генерируем один уровень детей для нод из списка
        cnt_nodes = 1  # счетчик кол-ва вершин

        while len(list_nodes) != 0:
            new_list_nodes = []  # храним всех детей, полученных на этом шаге

            for nd in list_nodes:
                # генерируем один уровень детей
                child_list = generator.generate_children(nd, charge)
                # если дети есть, то записываем их в dict[индекс родителя] = [[индекс ребенка, вес], ...]
                if child_list is not None:
                    for child in child_list:
                        child.index = cnt_nodes
                        cnt_nodes += 1
                        weight = child.penalty_ship1 + child.penalty_ship2 + child.penalty_extraorder + child.storing_cost
                        # it's for debug
                        # print(f'Parent node\n{nd}\nChild node\n{child}\n')

                        newNode = [child.index, weight]
                        graph[nd.index].insert(0, newNode)
                        all_nodes.append(child)
                    new_list_nodes += child_list

            list_nodes = new_list_nodes

        return Graph(cnt_nodes, graph, all_nodes)

    def __init__(self, V: int, graph: defaultdict[list], all_nodes: [Node]):
        self.V = V
        self.graph = graph

        self.all_nodes = all_nodes


    # вернуть ноду из графа или None, если ее не существует
    def node_exist(self, node: Node):
        for full_node in self.all_nodes:
            if node == full_node:
                return full_node
        return None
    

    def find_node_by_index(self, ind: int) -> Node:
        for node in self.all_nodes:
            if node.index == ind:
                return node
            

    def find_path(self, v, parent, lst_ind) -> list:
        if parent[v] == -1:
            return lst_ind[::-1]
        
        lst_ind.append(parent[v])
        return self.find_path(parent[v], parent, lst_ind)
    

    def optimalSolution(self, dist, parent):
        dist_dict = {}
        for i in range(len(dist)):
            distance = dist[i]
            node = self.find_node_by_index(i)
            if node.final:
                dist_dict[i] = distance
        
        optimal_final_ind = max(dist_dict, key=dist_dict.get)
        lst_ind = self.find_path(optimal_final_ind, parent, [optimal_final_ind])
        lst_nodes = [self.find_node_by_index(ind) for ind in lst_ind]

        return lst_nodes

    
    def printSolution(self, src, dist, parent):
            print("Vertex\tDistance\tPath")
            for i in range(len(dist)):
                print(f"{src} -> {i}\t{dist[i]}\t\t{self.printPath(i, parent)}")

    def printPath(self, v, parent):
        if v == -1:
            return str(v)
        return self.printPath(parent[v], parent) + ' -> ' + str(v)

    # The main function that calculates distances 
    # of shortest paths from src to all vertices. 
    # It is a O(ELogV) function
    def dijkstra(self, src: Node):

        V = self.V  # Get the number of vertices in graph
        dist = [float('inf')] * V   # dist values used to pick minimum 
                    # weight edge in cut
        parent = [-1] * V  # Initialize parent array to -1
 
        # minHeap represents set E
        minHeap = Heap()
 
        #  Initialize min heap with all vertices. 
        # dist value of all vertices
        for v in range(V):
            minHeap.array.append( minHeap.
                                newMinHeapNode(v, dist[v]))
            minHeap.pos.append(v)
 
        # Make dist value of src vertex as 0 so 
        # that it is extracted first
        minHeap.pos[src] = src
        dist[src] = 0
        minHeap.decreaseKey(src, dist[src])
 
        # Initially size of min heap is equal to V
        minHeap.size = V
 
        # In the following loop, 
        # min heap contains all nodes
        # whose shortest distance is not yet finalized.
        while minHeap.isEmpty() == False:
 
            # Extract the vertex 
            # with minimum distance value
            newHeapNode = minHeap.extractMin()
            u = newHeapNode[0]
 
            # Traverse through all adjacent vertices of 
            # u (the extracted vertex) and update their 
            # distance values
            for pCrawl in self.graph[u]:
 
                v = pCrawl[0]
 
                # If shortest distance to v is not finalized 
                # yet, and distance to v through u is less 
                # than its previously calculated distance
                if (minHeap.isInMinHeap(v) and
                     dist[u] != float('inf') and \
                   pCrawl[1] + dist[u] < dist[v]):
                        dist[v] = pCrawl[1] + dist[u]
                        parent[v] = u 
                        # update distance value 
                        # in min heap also
                        minHeap.decreaseKey(v, dist[v])
 
        self.printSolution(src, dist, parent)
        return self.optimalSolution(dist, parent)


    
    