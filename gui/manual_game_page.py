import sys
import tkinter as tk
from collections import OrderedDict

from classes.node import Node
from gui.utils import is_valid_input

LARGE_FONT = ("Raster Fonts", 24, '')
MIDDLE_FONT = ("Raster Fonts", 18, '')
SMALL_FONT = ("Raster Fonts", 12, '')

blue_color = 'blue3'
yellow_color = 'yellow'

even_design_params = {'foreground': 'black', 'background': 'turquoise'}
odd_design_params = {'background': blue_color, 'foreground': 'white'}


class GameGridColumn:
    def __init__(self, day_number: int, page: tk.Frame, previous_col=None):
        """ В previous_Node будут значения с прошлого дня – будем их использовать для вычислимых ячеек,
        Это или GameGridColumn или нода – надо решить"""

        # будем хранить оптимум тотал чарджа
        self.node = None
        self.optimal_total_charge = 0
        self.entries = OrderedDict()
        self.app = page.app
        self.day_number = day_number
        self.previous_col = previous_col

        color = 'black'
        if (day_number % 7) == page.app.parameters['first_sunday'].final_value:
            color = 'red'

        entry_params = {'master': page, 'width': 5, 'highlightthickness': 0}
        label_params = {'master': page, 'width': 5, 'text': "", "fg": "green"}
        # Entry для значения, Label – для оптимального решения
        self.entries['day'] = [tk.Entry(fg=color, **entry_params), tk.Label(**label_params)]
        self.entries['day'][0].insert(tk.END, string=str(day_number))

        self.entries['storing_mass'] = [tk.Entry(**entry_params, **odd_design_params), tk.Label(**label_params)]

        self.entries['ship1_mass'] = [tk.Entry(**entry_params), tk.Label(**label_params)]
        if day_number == int(self.app.parameters['day_ship1_arrival'].final_value):
            self.entries['ship1_mass'][0].config(text='0')

        self.entries['ship2_mass'] = [tk.Entry(**entry_params), tk.Label(**label_params)]
        if day_number == int(self.app.parameters['day_ship2_arrival'].final_value):
            self.entries['ship2_mass'][0].config(text='0')

        self.entries['day_order'] = [tk.Entry(**entry_params), tk.Label(**label_params)]
        self.entries['ship1_load'] = [tk.Entry(**entry_params), tk.Label(**label_params)]
        self.entries['ship2_load'] = [tk.Entry(**entry_params), tk.Label(**label_params)]

        self.entries['pen_ship1_unloading'] = [tk.Entry(**entry_params), tk.Label(**label_params)]
        self.entries['pen_ship2_unloading'] = [tk.Entry(**entry_params), tk.Label(**label_params)]
        self.entries['pen_extraorder'] = [tk.Entry(**entry_params), tk.Label(**label_params)]
        self.entries['storing_cost'] = [tk.Entry(**entry_params), tk.Label(**label_params)]
        self.entries['day_charges'] = [tk.Entry(**entry_params), tk.Label(**label_params)]
        self.entries['total_charges'] = [tk.Entry(**entry_params), tk.Label(**label_params)]

        for i, entry in enumerate(self.entries.values()):
            entry[0].config(state="readonly")
            entry[0].grid(row=i * 2 + 2, column=day_number, padx=0, pady=0)
            entry[1].grid(row=i * 2 + 3, column=day_number, padx=0, pady=0)

    def unblock(self):
        self.entries['day_order'][0].config(state='normal')
        self.entries['ship1_load'][0].config(state='normal')
        self.entries['ship2_load'][0].config(state='normal')

    def collect_user_input(self) -> bool:
        # одна нода в графе уже точно есть
        previous_node = self.app.nodes[-1]

        day_order = self.entries['day_order'][0].get()
        ship1_load = self.entries['ship1_load'][0].get()
        ship2_load = self.entries['ship2_load'][0].get()

        if not (is_valid_input(day_order) and is_valid_input(ship1_load) and is_valid_input(ship2_load)):
            print('returned false because of non digits')
            return False

        ship1_load = [0 if ship1_load == '' else int(ship1_load)][0]
        ship2_load = [0 if ship2_load == '' else int(ship2_load)][0]
        day_order = [0 if day_order == '' else int(day_order)][0]

        departed1 = (ship1_load == int(self.app.parameters['max_ship1'].final_value))
        departed2 = (ship2_load == int(self.app.parameters['max_ship2'].final_value))

        node = Node(
            day=self.day_number,
            arrive1=(int(self.app.parameters['day_ship1_arrival'].final_value) > self.day_number),
            arrive2=(int(self.app.parameters['day_ship2_arrival'].final_value) > self.day_number),
            ship1=ship1_load,
            ship2=ship2_load,
            departed1=departed1,
            departed2=departed2,
            warehouse=previous_node.warehouse + day_order - ship1_load - ship2_load + ship1_load + ship2_load,
            order=day_order
        )
        checked_node = self.app.graph.node_exist(node)
        # либо она None, либо она уже заполнена
        if checked_node:
            # self.update_totals(checked_node.day_charge)
            # уже посчитанная нода
            self.app.nodes.append(checked_node)
            self.node = checked_node
            return True
        print('Returned False because this node does not exists')
        return False

    def calculate_running_total(self, n_days: int) -> int:
        # result = 0
        # for node in self.app.nodes:
        #     result += node.daily_charges
        return sum(map(lambda node: node.daily_charges, self.app.nodes[:n_days]))

    def update_totals(self):
        print('updated values')
        if self.previous_col is not None:
            self.previous_col.entries['day_charges'][0].config(state='normal')
            self.previous_col.entries['day_charges'][0].insert(tk.END, string=self.node.daily_charge)

            # new_total_charges = 0
            # for i in range(self.day_number):
            #     new_total_charges += self.app.nodes[i].daily_charges
            self.previous_col.entries['total_charges'][0].config(state='normal')
            self.previous_col.entries['total_charges'][0].insert(tk.END,
                                                                 string=self.calculate_running_total(self.day_number))

    def show_optimum(self, optimum_node: Node, running_total: int):

        # for i, entry in enumerate(zip(self.entries.values()):
        #     entry[1].config(text='22')

        self.entries['ship1_mass'][1].config(text=optimum_node.ship1)
        self.entries['ship2_mass'][1].config(text=optimum_node.ship2)
        self.entries['day_order'][1].config(text=optimum_node.order)

        self.entries['ship1_load'][1].config(text='')
        self.entries['ship2_load'][1].config(text='')

        self.entries['pen_ship1_unloading'][1].config(text=optimum_node.penalty_ship1)
        self.entries['pen_ship2_unloading'][1].config(text=optimum_node.penalty_ship2)

        self.entries['pen_extraorder'][1].config(text=optimum_node.penalty_extraorder)
        self.entries['storing_cost'][1].config(text=optimum_node.storing_cost)

        self.entries['day_charges'][1].config(text=optimum_node.daily_charge)
        self.entries['total_charges'][1].config(text=running_total)


class ManualGamePage(tk.Frame):
    """
    в этот класс надо передавать список введенных пользователем значений, проверенных на валидность

    Класс итерируется по каждому параметру внутри каждого дня, давая пользователю возможность ввести значения там,
    где возможно по логике игры (с проверкой на валидность)

    В конце итерации внутри дня происходит подсчет daily charges и running total charges
    """

    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent, background='black')
        self.optimum_nodes = []
        self.end_the_game_button = None
        self.continue_button = None
        self.current_day = 0
        self.labels = []
        self.day_columns = []
        self.app = app
        self.n_rows = len(app.parameters)
        self.n_days = self.app.parameters['max_day'].final_value

        main_label = tk.Label(self, text="Play the game", width=50, font=LARGE_FONT, background=blue_color,
                              foreground=yellow_color)
        main_label.grid(row=1, column=0, sticky='n', columnspan=10)

        self.show_parameters()
        self.init_grid()

    def show_parameters(self):
        params = self.app.parameters
        common_design = {"width": 20, "anchor": "w", "wraplength": 200, "justify": "left"}
        self.labels = [
            tk.Label(self, text="Day (Sunday red)", **even_design_params, **common_design),
            tk.Label(self, text=f"Storing mass\n(at the end >= {params['storing_mass'].final_value})", **common_design,
                     **odd_design_params),
            tk.Label(self, text=f"Ship1 mass\n(at the end = {params['ship1_mass'].final_value}) ", **even_design_params,
                     **common_design),
            tk.Label(self, text=f"Ship2 mass\n(at the end = {params['ship2_mass'].final_value}) ", **common_design,
                     **odd_design_params),
            tk.Label(self, text=f"Day order\n(penalty, if order > {params['max_order'].final_value}) ",
                     **common_design, **even_design_params),
            tk.Label(self, text=f"Day load to ship1\n({params['min_ship1'].final_value} <= ld1 <= "
                                f"{params['max_ship1'].final_value})", **common_design, **odd_design_params),
            tk.Label(self, text=f"Day load to ship2\n({params['min_ship2'].final_value} <= ld1 <= "
                                f"{params['max_ship2'].final_value})", **common_design, **even_design_params),
            tk.Label(self, text=f"Penalty for ship1 unloading\n({params['penalty_ship1'].final_value}$/kt)",
                     **common_design, **odd_design_params),
            tk.Label(self, text=f"Penalty for ship2 unloading\n({params['penalty_ship2'].final_value}$/kt)",
                     **common_design, **even_design_params),
            tk.Label(self, text=f"Penalty for extra order\n({params['penalty_extraorder'].final_value}$/kt)",
                     **common_design, **odd_design_params),
            tk.Label(self, text=f"Storing cost ({params['storing_cost'].final_value}$/kt)",
                     **common_design, **even_design_params),
            tk.Label(self, text=f"Day charges ($)", **common_design, **odd_design_params),
            tk.Label(self, text=f"Total charges ($)", **common_design, **even_design_params),
        ]

        self.n_rows = len(self.labels)

        for i, label in enumerate(self.labels):
            label.grid(row=i * 2 + 2, column=0, pady=0, padx=0, rowspan=2)

    def init_grid(self):

        n_days = self.n_days
        n_params = self.n_rows
        print(f'Дней {self.n_rows}, параметров {n_params}')

        for i in range(n_days):
            previous_col = None
            if i != 0:
                previous_col = self.day_columns[-1]
            column = GameGridColumn(day_number=i + 1, page=self, previous_col=previous_col)
            self.day_columns.append(column)

        self.unblock_next_day()

        self.continue_button = tk.Button(self, text="Continue", command=self.unblock_next_day, activebackground='black',
                                         highlightbackground='black',
                                         background='black')
        self.continue_button.grid(row=self.n_rows * 2 + 2, columnspan=100)

    def unblock_next_day(self):
        if (self.current_day < self.n_days) and (self.current_day < len(self.day_columns)):
            current_column = self.day_columns[self.current_day]
            print(f'updated current column {self.current_day}')
            current_column.unblock()
            print(f'unblocked column {self.current_day}')

            user_input_check = current_column.collect_user_input()
            print(f'collected user input {self.current_day}, {user_input_check} check')

            if user_input_check:
                current_column.update_totals()
                print(f'updated totals {self.current_day}')

                self.current_day += 1
        else:
            self.show_optimal_solution()
            self.end_or_repeat()

    def show_optimal_solution(self):
        self.optimum_nodes = self.app.graph.optimalSolution()
        for i, col in enumerate(self.day_columns):
            col.set_optimum(self.optimum_nodes[i])
            col.show_optimum()

    def end_or_repeat(self):
        self.continue_button.configure(text="Try again")
        self.end_the_game_button = tk.Button(self, text="End the game", command=lambda: sys.exit(),
                                             activebackground='black',
                                             highlightbackground='black',
                                             background='black')
        self.end_the_game_button.grid(row=self.n_rows * 2 + 2, column=4, columnspan=100)
