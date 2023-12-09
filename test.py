from classes.node import Node
from classes.generateNode import GenerateNode
from classes.graph import Graph
from classes.charge import Charge

zero_node = Node(0, False, False, 0, 0, False, False, 1, 0)
generate = GenerateNode(1, 1, 1, 3, 1, 1, 2)
charge = Charge(1, 2, 2, 1, 2, 2, 2, 2, 2)

# res = generate.generate_children(zero_node, charge)
# for r in res:
#     print(r)
#     print()

Graph.create_from_node(zero_node, generate, charge)



