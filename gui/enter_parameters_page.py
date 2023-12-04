import tkinter as tk
from utils import check_input
from manual_game_page import ManualGamePage


class ParametersEntryPage(tk.Frame):
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)
        self.app = app

        main_label = tk.Label(self, text="Enter the game parameters", font=("Verdana", 24))
        main_label.grid(row=1, column=1, padx=10, pady=10, sticky='n')

        label_width = 30

        for row_number, text in enumerate(self.app.parameters.keys()):
            row_number_corrected = row_number + 2
            intro_text = tk.Label(self, text=text, width=label_width)
            entry = tk.Entry(self)
            label = tk.Label(self, text="", fg="red")

            intro_text.grid(row=row_number_corrected, column=0, padx=10, pady=5)
            entry.grid(row=row_number_corrected, column=1, padx=10, pady=5)
            label.grid(row=row_number_corrected, column=2, padx=10, pady=5)

            self.app.parameters[text] = [intro_text, entry, label]

        row_number_submit = len(self.app.parameters) + 2
        self.submit_button = tk.Button(self, text="Submit", command=self.submit)
        self.submit_button.grid(row=row_number_submit, columnspan=3)

    def submit(self):
        values = []
        for text, user_value, error_label in self.app.parameters.values():
            values.append(check_input(user_value, error_label))

        print(values)

        # если все параметры прошли проверку – переходим к игре
        if all(x is not None for x in values):
            self.app.show_frame(ManualGamePage)
