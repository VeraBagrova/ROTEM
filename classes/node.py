class Node:
    index = 0
    def __init__(self, day: int,
                 arrive1: bool, arrive2: bool,
                 ship1: int, ship2: int,
                 departed1: bool, departed2: bool,
                 warehouse: int, order: int) -> object:
        self.index = Node.index
        Node.index += 1
        self.day = day
        self.arrive1 = arrive1
        self.arrive2 = arrive2
        self.ship1 = ship1
        self.ship2 = ship2
        self.departed1 = departed1
        self.departed2 = departed2
        self.warehouse = warehouse
        self.order = order

        self.penalty_ship1 = 0
        self.penalty_ship2 = 0
        self.penalty_extraorder = 0
        self.storing_cost = 0

    def __str__(self):
        st = "day=" + str(self.day) + "\narrive1=" + str(self.arrive1) + "\narrive2=" + str(self.arrive2) + \
             "\nship1=" + str(self.ship1) + "\nship2=" + str(self.ship2) + "\ndeparted1=" + str(
            self.departed1) + "\ndeparted2=" + \
             str(self.departed2) + "\nwarehouse=" + str(self.warehouse) + "\norder=" + str(self.order)

        return st
