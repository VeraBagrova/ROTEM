import tkinter as tk

from classes.charge import Charge
from classes.generateNode import GenerateNode
from classes.graph import Graph
from classes.node import Node
from gui.utils import check_input
from gui.manual_game_page import ManualGamePage

blue_color = 'blue3'
yellow_color = 'yellow'

even_design_params = {'foreground': 'black', 'background': 'turquoise'}
odd_design_params = {'background': blue_color, 'foreground': 'white'}
# even_design_params = {}
# odd_design_params = {}

LARGE_FONT = ("Raster Fonts", 24, '')
MIDDLE_FONT = ("Raster Fonts", 18, '')
SMALL_FONT = ("Raster Fonts", 12, '')

width = 200
height = 150


class ParametersEntryPage(tk.Frame):
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent, background='black')
        self.app = app

        main_label = tk.Label(self, text="Play the game", font=LARGE_FONT, fg=yellow_color, bg=blue_color)
        main_label.grid(row=0, column=0, sticky='we', columnspan=3)

        label_width = 30

        for row_number, parameter in enumerate(self.app.get_parameters()):
            if row_number % 2 == 0:
                design_params = odd_design_params
            else:
                design_params = even_design_params

            # во втором row будем показывать оптимальное решение
            # row_number_corrected = (row_number + 2) * 2
            row_number_corrected = (row_number + 2)
            parameter.intro_text = tk.Label(
                self,
                design_params,
                text=parameter.description,
                width=label_width,
                anchor="w",
                wraplength=300,
                justify="left"
            )
            parameter.user_entry = tk.Entry(self, design_params, highlightthickness=0)
            if parameter.name == 'first_sunday':
                parameter.user_entry.insert(0, '3')
            else:
                parameter.user_entry.insert(0, '7')
            parameter.error_label = tk.Label(self, design_params, width=25, text="Ожидается ввод...", fg=yellow_color)
            parameter.optimal_solution = tk.Label(self, text="")

            parameter.intro_text.grid(row=row_number_corrected, column=0, padx=1, pady=1)
            parameter.user_entry.grid(row=row_number_corrected, column=1, padx=1, pady=1)
            parameter.error_label.grid(row=row_number_corrected, column=2, padx=1, pady=1)

        # row_number_submit = (len(self.app.parameters) * 2) + 4
        row_number_submit = len(self.app.parameters) + 2
        self.submit_button = tk.Button(self, text="Submit", command=self.submit, activebackground='black',
                                       highlightbackground='black',
                                       background='black')
        self.submit_button.grid(row=row_number_submit, columnspan=3)

    def submit(self):
        values = []
        for parameter in self.app.get_parameters():
            user_value, error_label = parameter.user_entry, parameter.error_label
            checked_value = check_input(user_value, error_label)
            if checked_value is not None:
                self.app.parameters[parameter.name].final_value = checked_value
            values.append(checked_value)

        print(values)

        # если все параметры прошли проверку – переходим к игре
        if all(x is not None for x in values):
            zero_node = Node(
                day=0,
                arrive1=False,
                arrive2=False,
                ship1=0,
                ship2=0,
                departed1=False,
                departed2=False,
                warehouse=self.app.parameters['warehouse'].final_value,
                order=0
            )
            generate = GenerateNode(
                storing_mass=self.app.parameters['storing_mass'].final_value,
                ship1_mass=self.app.parameters['ship1_mass'].final_value,
                ship2_mass=self.app.parameters['ship2_mass'].final_value,
                max_day=self.app.parameters['max_day'].final_value,
                day_ship1_arrival=self.app.parameters['day_ship1_arrival'].final_value,
                day_ship2_arrival=self.app.parameters['day_ship2_arrival'].final_value,
                first_sunday=self.app.parameters['first_sunday'].final_value
            )
            charge = Charge(
                min_ship1=self.app.parameters['min_ship1'].final_value,
                min_ship2=self.app.parameters['min_ship2'].final_value,
                penalty_ship1=self.app.parameters['penalty_ship1'].final_value,
                max_ship1=self.app.parameters['max_ship1'].final_value,
                max_ship2=self.app.parameters['max_ship2'].final_value,
                penalty_ship2=self.app.parameters['penalty_ship2'].final_value,
                max_order=self.app.parameters['max_order'].final_value,
                penalty_extraorder=self.app.parameters['penalty_extraorder'].final_value,
                storing_cost=self.app.parameters['storing_cost'].final_value
            )

            self.app.graph = Graph.create_from_node(zero_node, generate, charge)
            self.app.nodes = [zero_node]

            for PageLayout in [ManualGamePage]:
                frame = PageLayout(self.app.container, self.app)
                frame.grid(row=0, column=0, sticky='nsew')
                self.app.frames[PageLayout] = frame

            self.app.show_frame(ManualGamePage)
