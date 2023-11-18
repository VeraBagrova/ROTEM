from classes.node import Node
from classes.generateNode import GenerateNode

zero_node = Node(0, False, False, 0, 0, False, False, 6, 0)

generate = GenerateNode(10, 4, 6, 10, 2, 3)
res = generate.generate_children(zero_node)
for r in res:
    print(r)
    print()