import tkinter as tk

from classes.charge import Charge
from classes.generateNode import GenerateNode
from classes.graph import Graph
from classes.node import Node
from gui.utils import check_input
from gui.manual_game_page import ManualGamePage

# even_design_params = {'foreground': 'black', 'background': 'turquoise'}
# odd_design_params = {'background': 'dark blue', 'foreground': 'white'}
even_design_params = {}
odd_design_params = {}

width = 2000
height = 1500


class ParametersEntryPage(tk.Frame):
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent, width=width, height=height)
        self.app = app

        main_label = tk.Label(self, text="Enter the game parameters", font=("Verdana", 24))
        main_label.grid(row=1, column=1, padx=10, pady=10, sticky='n')

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
            parameter.user_entry = tk.Entry(self, design_params)
            if parameter.name == 'first_sunday':
                print('found sunday 1')
                parameter.user_entry.insert(0, '3')
            else:
                parameter.user_entry.insert(0, '7')
            parameter.error_label = tk.Label(self, design_params, text="", fg="red")
            parameter.optimal_solution = tk.Label(self, text="")

            parameter.intro_text.grid(row=row_number_corrected, column=0, padx=10, pady=5)
            parameter.user_entry.grid(row=row_number_corrected, column=1, padx=10, pady=5)
            parameter.error_label.grid(row=row_number_corrected, column=2, padx=10, pady=5)
            parameter.optimal_solution.grid(row=row_number_corrected + 1, column=2)

        # row_number_submit = (len(self.app.parameters) * 2) + 4
        row_number_submit = len(self.app.parameters) + 2
        self.submit_button = tk.Button(self, text="Submit", command=self.submit)
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
                warehouse=self.app.parameters['warehouse'].final_value,
                **Graph.zero_node_params
            )
            generate = GenerateNode(1, 1, 1, 3, 1, 1, 2)
            charge = Charge(1, 2, 2, 1, 2, 2, 2, 2, 2)

            self.app.graph = Graph.create_from_node(zero_node, generate, charge)

            for PageLayout in [ManualGamePage]:

                frame = PageLayout(self.app.container, self.app)
                frame.grid(row=0, column=0, sticky='nsew')
                self.app.frames[PageLayout] = frame

            self.app.show_frame(ManualGamePage)


