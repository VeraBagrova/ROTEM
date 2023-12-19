from classes.node import Node


class Charge:
    """
        Класс для расчета затрат:
        min(max)_ship1(2) – минимальное(максимальное) кол-во товаров, которое может быть загружено на корабль1(2)
        penalty_ship1(2) - штраф за непопадание в границы загрузки корабля1(2) - оплата за каждую единицу отклонения
        max_order - максимальное кол-во товаров, которое может быть заказано
        penalty_extraorder - штраф за превышение порога заказа - оплата за каждую единицу отклонения
        storing_cost - цена за хранение единицы товара на складе
    """

    def __init__(self,
                 min_ship1: int, max_ship1: int, penalty_ship1: int,
                 min_ship2: int, max_ship2: int, penalty_ship2: int,
                 max_order: int, penalty_extraorder: int,
                 storing_cost: int):
        self.min_ship1 = min_ship1
        self.max_ship1 = max_ship1
        self.penalty_ship1 = penalty_ship1
        self.min_ship2 = min_ship2
        self.max_ship2 = max_ship2
        self.penalty_ship2 = penalty_ship2
        self.max_order = max_order
        self.penalty_extraorder = penalty_extraorder
        self.storing_cost = storing_cost

    # обновляем параметры затрат в child_node
    def cnt_charge(self, parent_node: Node, child_node: Node):

        child_node.storing_cost = parent_node.warehouse * self.storing_cost
        child_node.penalty_extraorder = max(0, child_node.order - self.max_order) * self.penalty_extraorder

        ship1_load = child_node.ship1 - parent_node.ship1
        ship2_load = child_node.ship2 - parent_node.ship2

        # тут костыль с обновлением penalty_ship, не знаю, как его нормально оформить
        if child_node.arrive1 and not child_node.departed1:
            if ship1_load < self.min_ship1:
                child_node.penalty_ship1 = self.penalty_ship1 * (self.min_ship1 - ship1_load)

        if child_node.arrive2 and not child_node.departed2:
            if ship2_load < self.min_ship2:
                child_node.penalty_ship2 = self.penalty_ship2 * (self.min_ship2 - ship2_load)

        child_node.daily_charge = child_node.penalty_ship1 + child_node.penalty_ship2 + child_node.storing_cost + \
                                  child_node.penalty_extraorder

    def check_correct_node(self, parent_node: Node, child_node: Node) -> bool:
        ship1_load = child_node.ship1 - parent_node.ship1
        ship2_load = child_node.ship2 - parent_node.ship2

        if (ship1_load <= self.max_ship1) and (ship2_load <= self.max_ship2):
            return True
        return False
