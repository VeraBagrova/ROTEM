import tkinter as tk


class ManualGamePage(tk.Frame):
    """
    в этот класс надо передавать список введенных пользователем значений, проверенных на валидность

    Класс итерируется по каждому параметру внутри каждого дня, давая пользователю возможность ввести значения там,
    где возможно по логике игры (с проверкой на валидность)

    В конце итерации внутри дня происходит подсчет daily charges и running total charges
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='dark blue', width=600, height=600)
        self.controller = controller

        main_label = tk.Label(self, text="Start the game", font=("Verdana", 24))
        main_label.grid(row=1, column=1, padx=10, pady=10, sticky='n')



