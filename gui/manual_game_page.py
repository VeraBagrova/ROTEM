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

even_design_params_entry = {'disabledforeground': 'black', 'disabledbackground': 'turquoise', 'state': 'disabled',
                            'relief': 'flat'}
odd_design_params_entry = {'disabledbackground': blue_color, 'disabledforeground': 'white', 'state': 'disabled',
                           'relief': 'flat'}


class GameGridColumn:
    def __init__(self, day_number: int, page: tk.Frame):
        """ В previous_Node будут значения с прошлого дня – будем их использовать для вычислимых ячеек,
        Это или GameGridColumn или нода – надо решить"""

        # будем хранить оптимум тотал чарджа
        self.node = None
        self.optimal_total_charge = 0
        self.entries = OrderedDict()
        self.app = page.app
        self.page = page
        self.day_number = day_number

        bg_color = 'turquoise'
        fg_color = 'black'
        if (day_number % 7) == page.app.parameters['first_sunday'].final_value:
            fg_color = 'white'
            bg_color = 'red'

        entry_params = {'master': page, 'width': 5, 'highlightthickness': 0}
        label_params = {'master': page, 'width': 5, 'text': "", "fg": "green"}
        # Entry для значения, Label – для оптимального решения
        self.entries['day'] = [tk.Entry(**entry_params), tk.Label(**label_params)]
        self.entries['day'][0].insert(tk.END, string=str(day_number))

        self.entries['storing_mass'] = [tk.Entry(**entry_params, **odd_design_params), tk.Label(**label_params)]

        self.entries['ship1_mass'] = [tk.Entry(**entry_params), tk.Label(**label_params)]
        if day_number == int(self.app.parameters['day_ship1_arrival'].final_value):
            self.entries['ship1_mass'][0].insert(tk.END, string='0')

        self.entries['ship2_mass'] = [tk.Entry(**entry_params), tk.Label(**label_params)]
        if day_number == int(self.app.parameters['day_ship2_arrival'].final_value):
            self.entries['ship2_mass'][0].insert(tk.END, string='0')

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

            if i % 2 != 0:
                entry[0].config(**odd_design_params_entry)
                entry[1].config(**odd_design_params)
            else:
                entry[0].config(**even_design_params_entry)
                entry[1].config(**even_design_params)

            entry[0].grid(row=i * 2 + 2, column=day_number + 1, padx=1, pady=1)
            entry[1].grid(row=i * 2 + 3, column=day_number + 1, padx=0, pady=0)

        self.entries['day'][0].config(disabledforeground=fg_color, disabledbackground=bg_color)

    def unblock(self):
        self.entries['day_order'][0].config(state='normal', background=yellow_color, foreground='black')
        self.entries['ship1_load'][0].config(state='normal', background=yellow_color, foreground='black')
        self.entries['ship2_load'][0].config(state='normal', background=yellow_color, foreground='black')

    def block(self):
        self.entries['day_order'][0].config(state='readonly', foreground='white')
        self.entries['ship1_load'][0].config(state='readonly', foreground='white')
        self.entries['ship2_load'][0].config(state='readonly', foreground='white')

    def block_back(self):
        self.entries['day_order'][0].config(state='disabled')
        self.entries['ship1_load'][0].config(state='disabled')
        self.entries['ship2_load'][0].config(state='disabled')

    def clean(self):
        # очистка колонки
        for i, dict_item in enumerate(self.entries.items()):
            key, value = dict_item

            if key in ['day']:
                continue

            design = even_design_params_entry
            if i % 2 != 0:
                design = odd_design_params_entry

            value[0].config(state='normal')
            value[0].delete(0, tk.END)
            value[0].insert(index=0, string="")
            value[0].config(**design)

            ### оставляем нули в дни прибытия кораблей
            if self.day_number == self.app.parameters['day_ship1_arrival'].final_value:
                self.entries['ship1_mass'][0].config(state='normal')
                self.entries['ship1_mass'][0].delete(0, tk.END)
                self.entries['ship1_mass'][0].insert(tk.END, string='0')
                self.entries['ship1_mass'][0].config(**even_design_params_entry)
                continue

            if self.day_number == self.app.parameters['day_ship2_arrival'].final_value:
                self.entries['ship2_mass'][0].config(state='normal')
                self.entries['ship2_mass'][0].delete(0, tk.END)
                self.entries['ship2_mass'][0].insert(tk.END, string='0')
                self.entries['ship2_mass'][0].config(**odd_design_params_entry)
                continue

        self.node = None

    def collect_user_input(self) -> bool:

        previous_node = self.app.nodes[-1]

        day_order = self.entries['day_order'][0].get()
        ship1_load = self.entries['ship1_load'][0].get()
        ship2_load = self.entries['ship2_load'][0].get()

        if not (is_valid_input(day_order) and is_valid_input(ship1_load) and is_valid_input(ship2_load)):
            self.page.info_label.config(text='Parameters are non valid! Please, try again')
            return False

        day_order = [0 if day_order == '' else int(day_order)][0]
        ship1_load = [0 if ship1_load == '' else int(ship1_load)][0]
        ship2_load = [0 if ship2_load == '' else int(ship2_load)][0]

        print(self.app.parameters['max_ship1'].final_value)

        departed1 = (previous_node.ship1 == int(self.app.parameters['ship1_mass'].final_value))
        departed2 = (previous_node.ship2 == int(self.app.parameters['ship2_mass'].final_value))

        params = {
            "day": self.day_number,
            "arrive1": (self.app.parameters['day_ship1_arrival'].final_value < self.day_number),
            "arrive2": (self.app.parameters['day_ship2_arrival'].final_value < self.day_number),
            "ship1": previous_node.ship1 + ship1_load,
            "ship2": previous_node.ship2 + ship2_load,
            "departed1": departed1,
            "departed2": departed2,
            "warehouse": previous_node.warehouse + day_order - ship1_load - ship2_load,
            "order": day_order
        }

        node = Node(**params)
        checked_node = self.app.graph.node_exist(node)

        # либо она None, либо она уже заполнена
        if checked_node:
            # уже посчитанная нода
            self.app.nodes.append(checked_node)
            self.node = checked_node
            self.update_totals()
            return True

        self.page.info_label.config(text='Parameters are non valid! Please, try again')
        print('Returned False because this node does not exists')
        print(node)
        return False

    def calculate_running_total(self, n_days: int) -> int:
        return sum(map(lambda node: node.daily_charge, self.app.nodes[:n_days + 1]))

    def update_totals(self):

        self.entries['storing_mass'][0].config(state='normal')
        self.entries['storing_mass'][0].insert(tk.END, string=str(self.node.warehouse))
        self.entries['storing_mass'][0].config(**odd_design_params_entry)

        if self.day_number > self.app.parameters['day_ship1_arrival'].final_value:
            self.entries['ship1_mass'][0].config(state='normal')
            self.entries['ship1_mass'][0].insert(tk.END, string=str(self.node.ship1))
            self.entries['ship1_mass'][0].config(**even_design_params_entry)

        if self.day_number > self.app.parameters['day_ship2_arrival'].final_value:
            self.entries['ship2_mass'][0].config(state='normal')
            self.entries['ship2_mass'][0].insert(tk.END, string=str(self.node.ship2))
            self.entries['ship2_mass'][0].config(**odd_design_params_entry)

        self.entries['pen_ship1_unloading'][0].config(state='normal')
        self.entries['pen_ship1_unloading'][0].insert(tk.END, string=str(self.node.penalty_ship1))
        self.entries['pen_ship1_unloading'][0].config(**odd_design_params_entry)

        self.entries['pen_ship2_unloading'][0].config(state='normal')
        self.entries['pen_ship2_unloading'][0].insert(tk.END, string=str(self.node.penalty_ship2))
        self.entries['pen_ship2_unloading'][0].config(**even_design_params_entry)

        self.entries['pen_extraorder'][0].config(state='normal')
        self.entries['pen_extraorder'][0].insert(tk.END, string=str(self.node.penalty_extraorder))
        self.entries['pen_extraorder'][0].config(**odd_design_params_entry)

        self.entries['storing_cost'][0].config(state='normal')
        self.entries['storing_cost'][0].insert(tk.END, string=str(self.node.storing_cost))
        self.entries['storing_cost'][0].config(**even_design_params_entry)

        self.entries['day_charges'][0].config(state='normal')
        self.entries['day_charges'][0].insert(tk.END, string=self.node.daily_charge)
        self.entries['day_charges'][0].config(state='readonly')

        self.entries['total_charges'][0].config(state='normal')
        self.entries['total_charges'][0].insert(tk.END, string=str(self.calculate_running_total(self.day_number)))
        self.entries['total_charges'][0].config(state='readonly')

    def show_optimum(self, optimum_node: Node, running_total: int, ship1_load: int, ship2_load: int):

        design_params = {"background": 'green1', "foreground": 'black'}

        self.entries['storing_mass'][1].config(text=optimum_node.warehouse, **design_params)

        self.entries['ship1_load'][1].config(text=ship1_load, **design_params)
        self.entries['ship2_load'][1].config(text=ship2_load, **design_params)

        self.entries['ship1_mass'][1].config(text=optimum_node.ship1, **design_params)
        self.entries['ship2_mass'][1].config(text=optimum_node.ship2, **design_params)
        self.entries['day_order'][1].config(text=optimum_node.order, **design_params)

        self.entries['pen_ship1_unloading'][1].config(text=optimum_node.penalty_ship1, **design_params)
        self.entries['pen_ship2_unloading'][1].config(text=optimum_node.penalty_ship2, **design_params)

        self.entries['pen_extraorder'][1].config(text=optimum_node.penalty_extraorder, **design_params)
        self.entries['storing_cost'][1].config(text=optimum_node.storing_cost, **design_params)

        self.entries['day_charges'][1].config(text=optimum_node.daily_charge, **design_params)
        self.entries['total_charges'][1].config(text=running_total, **design_params)


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
        self.back_button = None
        self.info_label = None
        self.current_day = 0
        self.labels = []
        self.day_columns = []
        self.app = app
        self.n_rows = len(app.parameters)
        self.n_days = self.app.parameters['max_day'].final_value

        main_label = tk.Label(self, text="Play the game", font=LARGE_FONT, background=blue_color,
                              foreground=yellow_color)
        main_label.grid(row=1, column=0, sticky='we', columnspan=8)

        self.info_label = tk.Label(self, text="", activebackground='black',
                                   highlightbackground='black',
                                   background='black',
                                   fg='white')
        self.info_label.grid(row=self.n_rows * 2 + 3, columnspan=4)

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
            label.grid(row=i * 2 + 2, column=0, pady=1, padx=1, rowspan=2, sticky='ns')

    def init_grid(self):

        n_days = self.n_days
        n_params = self.n_rows
        print(f'Дней {self.n_rows}, параметров {n_params}')

        for i in range(1, n_days + 1):
            column = GameGridColumn(day_number=i, page=self)
            self.day_columns.append(column)

        # ublock the first day
        self.day_columns[0].unblock()
        self.continue_button = tk.Button(self,
                                         text="Continue",
                                         command=self.unblock_next_day,
                                         activebackground='black',
                                         highlightbackground='black',
                                         background='black')
        self.continue_button.grid(row=self.n_rows * 2 + 2, columnspan=4)

        self.back_button = tk.Button(self,
                                     text="Back",
                                     command=self.clean_day,
                                     activebackground='black',
                                     highlightbackground='black',
                                     background='black'
                                     )
        self.back_button.grid(row=self.n_rows * 2 + 2, columnspan=4, column=4)

    def unblock_next_day(self):

        if (self.current_day < self.n_days) and (self.current_day < len(self.day_columns)):
            current_column = self.day_columns[self.current_day]
            user_input_check = current_column.collect_user_input()

            if user_input_check:
                self.day_columns[self.current_day].block()
                self.current_day += 1
                if self.current_day < self.n_days:
                    self.day_columns[self.current_day].unblock()

        else:
            self.show_optimal_solution()
            self.end_or_repeat()

    def clean_day(self):
        ### если число заполненных равно номеру следующего дня
        if (len(self.app.nodes) == self.current_day + 1) and (len(self.app.nodes) > 1):
            self.app.nodes.pop()
            self.day_columns[self.current_day].clean()
            self.day_columns[self.current_day].block_back()
            self.day_columns[self.current_day - 1].clean()
            self.day_columns[self.current_day - 1].unblock()

            print('cleaned the node', self.current_day + 1)
            self.current_day -= 1

    def show_optimal_solution(self):
        self.optimum_nodes = self.app.graph.dijkstra(self.app.nodes[0].index)
        total = 0
        prev_ship1_load = 0
        prev_ship2_load = 0
        for i, col in enumerate(self.day_columns):
            total += self.optimum_nodes[i].daily_charge
            ship1_load = self.optimum_nodes[i].ship1 - prev_ship1_load
            ship2_load = self.optimum_nodes[i].ship2 - prev_ship2_load
            col.show_optimum(self.optimum_nodes[i], total, ship1_load, ship2_load)
            prev_ship1_load = self.optimum_nodes[i].ship1
            prev_ship2_load = self.optimum_nodes[i].ship2

    def start_over(self):
        for PageLayout in [ManualGamePage]:
            frame = PageLayout(self.app.container, self.app)
            frame.grid(row=0, column=0, sticky='nsew')
            self.app.frames[PageLayout] = frame

        self.app.show_frame(ManualGamePage)

    def end_or_repeat(self):
        self.continue_button.configure(text="Try again", command=self.start_over)
        self.end_the_game_button = tk.Button(self,
                                             text="End the game",
                                             command=lambda: sys.exit(),
                                             activebackground='black',
                                             highlightbackground='black',
                                             background='black'
                                             )
        self.end_the_game_button.grid(row=self.n_rows * 2 + 2, column=4, columnspan=3)
