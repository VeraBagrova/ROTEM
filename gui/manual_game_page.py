import sys
import tkinter as tk
from collections import OrderedDict


class GameGridColumn:
    def __init__(self, day_number: int, page: tk.Frame, previous_node = None):
        """ В previous_Node будут значения с прошлого дня – будем их использовать для вычислимых ячеек,
        Это или GameGridColumn или нода – надо решить"""

        self.entries = OrderedDict()
        self.previous_col = previous_node

        color = 'black'
        if (day_number % 7) == page.app.parameters['first_sunday'].final_value:
            color = 'red'

        entry_params = {'master': page, 'width': 5}
        label_params = {'master': page, 'text': "", "fg":"green"}
        # Entry для значения, Label – для оптимального решения
        self.entries['day'] = [tk.Entry(fg=color, **entry_params), tk.Label(**label_params)]
        self.entries['day'][0].insert(tk.END, string=str(day_number))

        self.entries['storing_mass'] = [tk.Entry(**entry_params), tk.Label(**label_params)]
        self.entries['ship1_mass'] = [tk.Entry(**entry_params), tk.Label(**label_params)]
        self.entries['ship2_mass'] = [tk.Entry(**entry_params), tk.Label(**label_params)]

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
            entry[0].grid(row=i * 2 + 2, column=day_number, padx=5, pady=0)
            entry[1].grid(row=i * 2 + 3, column=day_number, padx=5, pady=0)

    def unblock(self):
        self.entries['day_order'][0].config(state='normal')
        self.entries['ship1_load'][0].config(state='normal')
        self.entries['ship2_load'][0].config(state='normal')

    def collect_user_input(self) -> bool:
        day_order = self.entries['day_order'][0].get()
        ship1_load = self.entries['ship1_load'][0].get()
        ship2_load = self.entries['ship2_load'][0].get()
        # дальше запускаем проверку – может ли существовать нода с такими значениями
        return True

    def update_totals(self):
        print('updated values')
        if self.previous_col is not None:
            self.previous_col.entries['day_charges'][0].config(state='normal')
            self.previous_col.entries['day_charges'][0].insert(tk.END, string='new total')
            # тотал пересчитаем на основе previous_node
            self.previous_col.entries['total_charges'][0].insert(tk.END, string=f'totals')

    def show_optimum(self):
        for i, entry in enumerate(self.entries.values()):
            entry[1].config(text='22')


class ManualGamePage(tk.Frame):
    """
    в этот класс надо передавать список введенных пользователем значений, проверенных на валидность

    Класс итерируется по каждому параметру внутри каждого дня, давая пользователю возможность ввести значения там,
    где возможно по логике игры (с проверкой на валидность)

    В конце итерации внутри дня происходит подсчет daily charges и running total charges
    """

    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)
        self.end_the_game_button = None
        self.continue_button = None
        self.current_day = 0
        self.labels = []
        self.day_columns = []
        self.app = app
        self.n_rows = len(app.parameters)
        self.n_days = self.app.parameters['max_day'].final_value

        main_label = tk.Label(self, text="Play the game", width=50, font=("Verdana", 24))
        main_label.grid(row=1, column=0, padx=10, pady=0, sticky='n', columnspan=100)

        self.show_parameters()
        self.init_grid()

    def show_parameters(self):
        params = self.app.parameters
        common_design = {"width": 20, "anchor": "w", "wraplength": 200, "justify": "left"}
        self.labels = [
            tk.Label(self, text="Day (Sunday red)", **common_design),
            tk.Label(self, text=f"Storing mass\n(at the end >= {params['storing_mass'].final_value})", **common_design),
            tk.Label(self, text=f"Ship1 mass\n(at the end = {params['ship1_mass'].final_value}) ", **common_design),
            tk.Label(self, text=f"Ship2 mass\n(at the end = {params['ship2_mass'].final_value}) ", **common_design),
            tk.Label(self, text=f"Day order\n(penalty, if order > {params['max_order'].final_value}) ",
                     **common_design),
            tk.Label(self, text=f"Day load to ship1\n({params['min_ship1'].final_value} <= ld1 <= "
                                f"{params['max_ship1'].final_value})", **common_design),
            tk.Label(self, text=f"Day load to ship2\n({params['min_ship2'].final_value} <= ld1 <= "
                                f"{params['max_ship2'].final_value})", **common_design),
            tk.Label(self, text=f"Penalty for ship1 unloading\n({params['penalty_ship1'].final_value}$/kt)",
                     **common_design),
            tk.Label(self, text=f"Penalty for ship2 unloading\n({params['penalty_ship2'].final_value}$/kt)",
                     **common_design),
            tk.Label(self, text=f"Penalty for extra order\n({params['penalty_extraorder'].final_value}$/kt)",
                     **common_design),
            tk.Label(self, text=f"Storing cost ({params['storing_cost'].final_value}$/kt)",
                     **common_design),
            tk.Label(self, text=f"Day charges ($)", **common_design),
            tk.Label(self, text=f"Total charges ($)", **common_design),
        ]

        self.n_rows = len(self.labels)

        for i, label in enumerate(self.labels):
            label.grid(row=i * 2 + 2, column=0, pady=0, padx=5)

    # def show_days(self):
    #     for day_number in range(self.n_days):
    #         color = 'black'
    #         if (day_number % 7) == self.app.parameters['first_sunday'].final_value:
    #             print('found sunday 2')
    #             color = 'red'
    #         day = tk.Entry(self, fg=color, width=5)
    #         day.insert(tk.END, string=str(day_number))
    #         day.config(state="readonly")
    #         day.grid(row=2, column=day_number + 1, padx=5, pady=5)

    def init_grid(self):

        n_days = self.n_days
        n_params = self.n_rows
        print(f'Дней {self.n_rows}, параметров {n_params}')

        for i in range(n_days):
            previous_node = None
            if i != 0:
                previous_node = self.day_columns[-1]
            print(i + 1, previous_node)
            column = GameGridColumn(day_number=i + 1, page=self, previous_node=previous_node)
            self.day_columns.append(column)

        self.unblock_next_day()

        self.continue_button = tk.Button(self, text="Continue", command=self.unblock_next_day)
        self.continue_button.grid(row=self.n_rows * 2 + 2, columnspan=100)

    def unblock_next_day(self):
        if (self.current_day < self.n_days) and (self.current_day < len(self.day_columns)):
            current_column = self.day_columns[self.current_day]
            current_column.unblock()
            user_input_check = current_column.collect_user_input()
            if user_input_check:
                current_column.update_totals()
                self.current_day += 1
        else:
            self.show_optimal_solution()
            self.end_or_repeat()

    def show_optimal_solution(self):
        for col in self.day_columns:
            col.show_optimum()

    def end_or_repeat(self):
        self.continue_button.configure(text="Try again")
        self.end_the_game_button = tk.Button(self, text="End the game", command=lambda: sys.exit())
        self.end_the_game_button.grid(row=self.n_rows * 2 + 2, column=4, columnspan=100)
