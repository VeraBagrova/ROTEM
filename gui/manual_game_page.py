import tkinter as tk
from collections import OrderedDict


class GameGridColumn:
    def __init__(self, day_number: int, n_col: int, page: tk.Frame, previous_node = None):
        """ В previous_Node будут значения с прошлого дня – будем их использовать для вычислимых ячеек"""

        self.entries = OrderedDict()

        color = 'black'
        if (day_number % 7) == page.app.parameters['first_sunday'].final_value:
            print('found sunday 2')
            color = 'red'

        self.entries['day'] = tk.Entry(page, fg=color, width=5)
        self.entries['day'].insert(tk.END, string=str(day_number))

        self.entries['storing_mass'] = tk.Entry(page, width=5)
        self.entries['ship1_mass'] = tk.Entry(page, width=5)
        self.entries['ship2_mass'] = tk.Entry(page, width=5)

        self.entries['day_order'] = tk.Entry(page, width=5)
        self.entries['ship1_load'] = tk.Entry(page, width=5)
        self.entries['ship2_load'] = tk.Entry(page, width=5)

        self.entries['pen_ship1_unloading'] = tk.Entry(page, width=5)
        self.entries['pen_ship2_unloading'] = tk.Entry(page, width=5)
        self.entries['pen_extraorder'] = tk.Entry(page, width=5)
        self.entries['storing_cost'] = tk.Entry(page, width=5)
        self.entries['day_charges'] = tk.Entry(page, width=5)
        self.entries['total_charges'] = tk.Entry(page, width=5)

        for i, entry in enumerate(self.entries.values()):
            entry.config(state="readonly")
            entry.grid(row=i + 2, column=n_col, padx=5, pady=5)

    def unblock(self):
        self.entries['day_order'].config(state='normal')
        self.entries['ship1_load'].config(state='normal')
        self.entries['ship2_load'].config(state='normal')

    def collect_user_input(self):
        day_order = self.entries['day_order'].get()
        ship1_load = self.entries['ship1_load'].get()
        ship2_load = self.entries['ship2_load'].get()
        # дальше запускаем проверку – может ли существовать нода с такими значениями


class ManualGamePage(tk.Frame):
    """
    в этот класс надо передавать список введенных пользователем значений, проверенных на валидность

    Класс итерируется по каждому параметру внутри каждого дня, давая пользователю возможность ввести значения там,
    где возможно по логике игры (с проверкой на валидность)

    В конце итерации внутри дня происходит подсчет daily charges и running total charges
    """

    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)
        self.continue_button = None
        self.current_day = 0
        self.labels = []
        self.day_columns = []
        self.app = app
        self.n_rows = len(app.parameters)
        self.n_days = self.app.parameters['max_day'].final_value

        main_label = tk.Label(self, text="Start the game", width=50, font=("Verdana", 24))
        main_label.grid(row=1, column=0, padx=10, pady=10, sticky='n', columnspan=100)

        self.show_parameters()
        self.init_grid()

    def show_parameters(self):
        params = self.app.parameters
        common_design = {"width": 18, "anchor": "w", "wraplength": 150, "justify": "left"}
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
            label.grid(row=i + 2, column=0, pady=5, padx=5)

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
            self.day_columns.append(GameGridColumn(day_number=self.current_day,
                                    n_col=i + 1,
                                    page=self))

        self.continue_button = tk.Button(self, text="Continue", command=self.unblock_next_day)
        self.continue_button.grid(row=self.n_rows + 2, columnspan=100)

        return

    def unblock_next_day(self):
        if self.current_day < self.n_days:
            print(f"Columns amount {len(self.day_columns)}, current day {self.current_day}")
            current_column = self.day_columns[self.current_day]
            current_column.unblock()
            current_column.collect_user_input()
            self.current_day += 1
        else:
            self.show_optimal_solution()

    def show_optimal_solution(self):
        pass
