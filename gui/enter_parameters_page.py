import tkinter as tk
from utils import check_input
from manual_game_page import ManualGamePage


class ParametersEntryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        main_label = tk.Label(self, text="Enter the game parameters", font=("Verdana", 24))
        main_label.grid(row=1, column=1, padx=10, pady=10, sticky='n')

        label_width = 30

        self.row_content = []
        self.parameters = ['Amount of days under control',
                           'Number of the first Sunday',
                           'Storing mass at the end',
                           'Ship 1 mass at the end',
                           'Ship 2 mass at the end',
                           'Upper limit for order (penalty if exceeded)',
                           'Day load to ship 1 (lower limit)',
                           'Day load to ship 1 (upper limit)',
                           'Day load to ship 2 (lower limit)',
                           'Day load to ship 2 (upper limit)',
                           'Penalty for ship 1 unloading',
                           'Penalty for ship 2 unloading',
                           'Penalty for extra order',
                           'Storing cost']
        for row_number, text in enumerate(self.parameters):
            row_number_corrected = row_number + 2
            intro_text = tk.Label(self, text=text, width=label_width)
            entry = tk.Entry(self)
            label = tk.Label(self, text="", fg="red")

            intro_text.grid(row=row_number_corrected, column=0, padx=10, pady=5)
            entry.grid(row=row_number_corrected, column=1, padx=10, pady=5)
            label.grid(row=row_number_corrected, column=2, padx=10, pady=5)

            self.row_content.append([intro_text, entry, label])

        row_number_submit = len(self.row_content) + 2
        self.submit_button = tk.Button(self, text="Submit", command=self.submit)
        self.submit_button.grid(row=row_number_submit, columnspan=3)

    def submit(self):
        values = []
        for row in self.row_content:
            values.append(check_input(row[1], row[2]))

        print(values)

        # если все параметры прошли проверку – переходим к игре
        if all(x is not None for x in values):
            self.controller.show_frame(ManualGamePage)
