import tkinter as tk
from tkinter import ttk
from typing import Tuple, List
from enter_parameters_page import ParametersEntryPage
from manual_game_page import ManualGamePage
from utils import GameParameterStorage

LARGE_FONT = ("Times New Roman", 24, '')
MIDDLE_FONT = ("Times New Roman", 18, '')
SMALL_FONT = ("Times New Roman", 12, '')

width = 2000
height = 1500


class TkinterApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self, width=width, height=height)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        params = {
            'max_day': 'Amount of days under control',
            'first_sunday': 'Number of the first Sunday',
            'warehouse': 'Starting storing mass',
            'storing_mass': 'Storing mass at the end',
            "ship1_mass": 'Ship 1 mass at the end',
            "ship2_mass": 'Ship 2 mass at the end',
            "max_order": 'Upper limit for order (penalty if exceeded)',
            "min_ship1": 'Day load to ship 1 (lower limit)',
            "max_ship1": 'Day load to ship 1 (upper limit)',
            "min_ship2": 'Day load to ship 2 (lower limit)',
            "max_ship2": 'Day load to ship 2 (upper limit)',
            "penalty_ship1": 'Penalty for ship 1 unloading',
            "penalty_ship2": 'Penalty for ship 2 unloading',
            "penalty_extraorder": 'Penalty for extra order',
            "storing_cost": 'Storing cost'
        }

        self.parameters = {name: GameParameterStorage(name=name, description=text) for name, text in params.items()}

        self.frames = {}

        for PageLayout in (StartPage, ParametersEntryPage, ManualGamePage):
            # вызываем конструктор каждой из страниц
            frame = PageLayout(container, self)
            self.frames[PageLayout] = frame

        self.show_frame(StartPage)

    def show_frame(self, frame_to_show):
        frame = self.frames[frame_to_show]
        frame.tkraise()

    def get_parameters(self) -> List[GameParameterStorage]:
        return list(self.parameters.values())


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=width, height=height)
        label = ttk.Label(
            self,
            text="HARBOUR STORE MANAGEMENT",
            font=LARGE_FONT,
            # foreground='yellow',
            # background='dark blue'
        )
        label.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            columnspan=2,
        )

        with open('gui/intro.txt', 'r') as file:
            intro = file.read()

        intro_label = ttk.Label(
            self,
            text=intro,
            font=SMALL_FONT,
            width=100,
            # foreground='yellow',
            # background='dark blue'
        )
        intro_label.grid(
            row=1,
            column=0,
            padx=10,
            pady=10,
        )

        enter_the_data = ttk.Button(
            self,
            text="Enter the data",
            command=lambda: controller.show_frame(ParametersEntryPage)
        )
        enter_the_data.grid(
            row=2,
            column=0,
            padx=10,
            pady=10
        )


# class EnterTheDataPage(tk.Frame):
#     def check_number(self, entry_text: str):
#         self.error_label = tk.Label()
#         try:
#             number = int(entry_text)
#             if number < 2 or number > 14:
#                 self.error_label.config(text="Число должно быть от 2 до 14", fg="red")
#             else:
#                 self.error_label.config(text="")
#         except ValueError:
#             self.error_label.config(text="Введите корректное число", fg="red")
#
#     def on_entry_change(self, *args):
#         self.check_number(self.days_entry.get())
#
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         label = ttk.Label(self, text="Enter the Data", font=LARGEFONT)
#         label.grid(row=1, column=1, padx=10, pady=10, sticky='n')
#
#         label = ttk.Label(self, text="Enter amount of days under control", font=MIDDLEFONT)
#         label.grid(row=2, column=1, padx=10, pady=10, sticky='n')
#
#         self.days_entry = tk.Entry(self, width=40, state='normal', validate="key",
#                                    validatecommand=self.on_entry_change)
#
#         self.days_entry.grid(row=3, column=1, padx=10, pady=10)

# amount_of_days = collect_entry_message(days_entry)
# while amount_of_days:
#     days_entry = tk.Entry(self, width=40, state='enabled')

# for i in range(12):
#     for j in range(6):
#         # Create entry cell with some text inside
#         entry = tk.Entry(self, width=10)
#         entry.insert(tk.END, f"Row {i}, Column {j}")
#         entry.grid(row=4 + i, column=j, padx=10, pady=10)

# entry = tk.Entry(self, width=40, foreground='black', background='turquoise')
# entry.insert(tk.END, f"Day (Sunday Red) ")
# entry.grid(row=0, column=0, padx=2)
#
# entry = tk.Entry(self, width=40, background='dark blue', foreground='white')
# entry.insert(tk.END, "Storing mass at the end should be equal or more than ")
# entry.grid(row=1, column=0, padx=2)
#
# entry = tk.Entry(self, width=40, foreground='black', background='turquoise')
# entry.insert(tk.END, "Ship 1 mass at the end should be equal to  ")
# entry.grid(row=2, column=0, padx=2)
#
# entry = tk.Entry(self, width=40, background='dark blue', foreground='white')
# entry.insert(tk.END, "Ship 2 mass at the end should be equal to  ")
# entry.grid(row=3, column=0, padx=2)
#
# entry = tk.Entry(self, width=40, foreground='black', background='turquoise')
# entry.insert(tk.END, "Day load to ship 1 left and right limits: ")
# entry.grid(row=4, column=0, padx=2)
#
# entry = tk.Entry(self, width=40, background='dark blue', foreground='white')
# entry.insert(tk.END, "Day load to ship 2 left and right limits: ")
# entry.grid(row=5, column=0, padx=2)
#
# entry = tk.Entry(self, width=40, foreground='black', background='turquoise')
# entry.insert(tk.END, "Penalty for ship1 unloading ")
# entry.grid(row=6, column=0, padx=2)
#
# for i in range(7):
#     for j in range(6):
#         # Create entry cell with some text inside
#         if i % 2 == 0:
#             entry = tk.Entry(self, width=15, foreground='black', background='turquoise')
#         else:
#             entry = tk.Entry(self, width=15, foreground='white', background='dark blue')
#
#         entry.insert(tk.END, f" ")
#         entry.grid(row=i, column=1 + j, padx=2)
#
# next_button = ttk.Button(
#     self,
#     text="Back",
#     command=lambda: controller.show_frame(Page2)
# )
# opt_button = ttk.Button(
#     self,
#     text="Optimal solution",
#     command=lambda: controller.show_frame(Page2)
# )
# next_button.grid(row=7, column=1, columnspan=2, pady=12)
# opt_button.grid(row=7, column=4, columnspan=2, pady=12)
# intro_label = ttk.Label(self, text=intro, font=SMALLFONT, width=100)
# intro_label.grid(row=10, column=1, padx=10, pady=10, sticky="w")
#
# # button to show frame 2 with text
# # layout2
# button1 = ttk.Button(self, text="Enter the data",
#                      command=lambda: controller.show_frame(StartPage))
#
# # putting the button in its place
# # by using grid
# button1.grid(row=12, column=1, padx=10, pady=10)


# button to show frame 2 with text
# layout2
# button2 = ttk.Button(self, text="Page 2",
#                      command=lambda: controller.show_frame(Page2))

# putting the button in its place by
# using grid
# button2.grid(row=2, column=1, padx=10, pady=10)


app = TkinterApp()
app.mainloop()
