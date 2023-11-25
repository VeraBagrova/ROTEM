from classes.node import Node 
from classes.charge import Charge 


class GenerateNode:

    '''
        storing mass – сколько должно быть товаров на складе на последний день
        ship1(2)_mass - сколько товаров должно быть на корабле1(2) для отправления
        max_day - количество дней, через которое мы должны закончить
        day_ship1(2)_arrival - номера дней, в которые пришли корабли
    '''

    def __init__(self, storing_mass: int, ship1_mass: int, ship2_mass: int, 
                 max_day: int, day_ship1_arrival: int, day_ship2_arrival):
        self.storing_mass = storing_mass
        self.ship1_mass = ship1_mass
        self.ship2_mass = ship2_mass
        self.max_mass = storing_mass + ship1_mass + ship2_mass
        
        self.max_day = max_day
        self.day_ship1_arrival = day_ship1_arrival
        self.day_ship2_arrival = day_ship2_arrival



    # генерируем один уровень вершин, то есть получили на вход одну и возвращаем всех возможных ее детей
    def generate_children(self, node: Node, charge: Charge) -> list[Node]:

        # расставляем флаги прибытия и отбытия кораблей
        def check_arrive_depart(day: int, day_ship_arrival: int, ship_mass: int) -> (bool, bool):
            arrive, departed = False, False
            if day >= day_ship_arrival:
                arrive = True
            if node.ship1 == ship_mass:
                departed = True
            
            return arrive, departed
        
        # вычисляем загруженность корабля, по которой будем итерироваться с учетом статуса прибытия
        def ship_iteration_borders(arrive: bool, ship: int, ship_mass: int) -> (int, int):
            if arrive:
                return ship, ship_mass + 1
            return 0, 1

        # create empty list to append nodes
        node_lst = []
        # stop generation if reach max day
        day = node.day + 1
        if day > self.max_day:
            return None
        
        # create arrive and departed flags for current day
        arrive1, departed1 = check_arrive_depart(day, self.day_ship1_arrival, self.ship1_mass)
        arrive2, departed2 = check_arrive_depart(day, self.day_ship2_arrival, self.ship2_mass)

        ship1_min, ship1_max = ship_iteration_borders(arrive1, node.ship1, self.ship1_mass)
        ship2_min, ship2_max = ship_iteration_borders(arrive2, node.ship2, self.ship2_mass)

        order = 0
        # sum of all products (ships, warehouse) not more than max mass
        while node.warehouse + order + node.ship1 + node.ship2 <= self.max_mass:
            for ship1 in range(ship1_min, ship1_max):
                for ship2 in range(ship2_min, ship2_max):
                    # cnt new warehouse
                    warehouse = node.warehouse + order - ship1 - ship2 + node.ship1 + node.ship2
                    if warehouse >= 0:
                        if not ( (ship1 == node.ship1) 
                                & (ship2 == node.ship2) 
                                & (warehouse == node.warehouse)):
                            new_node = Node(day, arrive1, arrive2, ship1, ship2, departed1, departed2, warehouse, order)
                            charge.cnt_charge(node, new_node) # обновляем затраты в ноде
                            node_lst.append(new_node)
            order += 1

        return node_lst


        
        
