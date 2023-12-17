from classes.node import Node
from classes.generateNode import GenerateNode
from classes.graph import Graph
from classes.charge import Charge

zero_node = Node(
    day=0,
    arrive1=False,
    arrive2=False,
    ship1=0,
    ship2=0,
    departed1=False,
    departed2=False,
    warehouse=1,
    order=0)
generate = GenerateNode(storing_mass=1,
                        ship1_mass=1,
                        ship2_mass=1,
                        max_day=3,
                        day_ship1_arrival=1,
                        day_ship2_arrival=1,
                        first_sunday=2)
charge = Charge(min_ship1=1,
                max_ship1=2,
                penalty_ship1=2,
                min_ship2=1,
                max_ship2=2,
                penalty_ship2=2,
                max_order=2,
                penalty_extraorder=2,
                storing_cost=2)

# res = generate.generate_children(zero_node, charge)
# for r in res:
#     print(r)
#     print()

Graph.create_from_node(zero_node, generate, charge)



