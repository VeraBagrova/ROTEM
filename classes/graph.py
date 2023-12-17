from classes.node import Node
from classes.generateNode import GenerateNode
from classes.charge import Charge
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
    zero_node_params = {
        "day": 0,
        "arrive1": False,
        "arrive2": False,
        "ship1": 0,
        "ship2": 0,
        "departed1": False,
        "departed2": False,
        "order": 0
    }

    # метод, генерирующий полный граф из нулевой вершины
    @classmethod
    def create_from_node(cls, node: Node, generator: GenerateNode, charge: Charge):
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
                        cnt_nodes += 1
                        weight = child.penalty_ship1 + child.penalty_ship2 + child.penalty_extraorder + child.storing_cost
                        # it's for debug
                        # print(f'Parent node\n{nd}\nChild node\n{child}\n')

                        newNode = [child.index, weight]
                        graph[nd.index].insert(0, newNode)
                    new_list_nodes += child_list

            list_nodes = new_list_nodes

        return Graph(cnt_nodes, graph)

    def __init__(self, V, graph: defaultdict[list]):
        self.V = V
        self.graph = graph
