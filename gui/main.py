import tkinter as tk
from tkinter import ttk
from typing import Tuple
from enter_parameters_page import ParametersEntryPage
from manual_game_page import ManualGamePage

LARGEFONT = ("Verdana", 36)
MIDDLEFONT = ("Verdana", 24)
SMALLFONT = ("Verdana", 12)


class tkinterApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self, width=600, height=600)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.parameters = {key: None for key in ['Amount of days under control',
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
                                                 'Storing cost']}

        self.frames = {}

        for PageLayout in (StartPage, ParametersEntryPage, ManualGamePage):
            # вызываем конструктор каждой из страниц
            frame = PageLayout(container, self)
            self.frames[PageLayout] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, frame_to_show):
        # наверное здесь можно закодить передачу аргументов в новую страницу
        frame = self.frames[frame_to_show]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Intro page", font=LARGEFONT)
        label.grid(row=1, column=1, padx=10, pady=10, sticky='n')

        with open('gui/intro.txt', 'r') as file:
            intro = file.read()

        intro_label = ttk.Label(self, text=intro, font=SMALLFONT, width=100)
        intro_label.grid(row=10, column=1, padx=10, pady=10, sticky="w")

        enter_the_data = ttk.Button(self, text="Enter the data",
                                    # command=lambda: controller.show_frame(EnterTheDataPage))
                                    command=lambda: controller.show_frame(ParametersEntryPage))
        enter_the_data.grid(row=12, column=1, padx=10, pady=10)


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

# entry = tk.Entry(self, width=40, state='disabled')
# entry.insert(tk.END, f"Day (Sunday Red) ")
# entry.grid(row=4, column=1, padx=10, pady=10)
#
# entry = tk.Entry(self, width=40, state='disabled')
# entry.insert(tk.END, "Storing mass at the end should be equal or more than ")
# entry.grid(row=6, column=1, padx=10, pady=10)
#
# entry = tk.Entry(self, width=40, state='disabled')
# entry.insert(tk.END, "Ship 1 mass at the end should be equal to  ")
# entry.grid(row=8, column=1, padx=10, pady=10)
#
# entry = tk.Entry(self, width=40, state='disabled')
# entry.insert(tk.END, "Ship 2 mass at the end should be equal to  ")
# entry.grid(row=10, column=1, padx=10, pady=10)
#
# entry = tk.Entry(self, width=40, state='disabled')
# entry.insert(tk.END, "Day load to ship 1 left and right limits: ")
# entry.grid(row=12, column=1, padx=10, pady=10)
#
# entry = tk.Entry(self, width=40)
# entry.insert(tk.END, "Day load to ship 2 left and right limits: ")
# entry.grid(row=14, column=1, padx=10, pady=10)
#
# entry = tk.Entry(self, width=40)
# entry.insert(tk.END, "Penalty for ship1 unloading ")
# entry.grid(row=16, column=1, padx=10, pady=10)
#
# for i in range(7):
#     for j in range(6):
#         # Create entry cell with some text inside
#         entry = tk.Entry(self, width=10)
#         entry.insert(tk.END, f" ")
#         entry.grid(row=4 + i * 2, column=2 + j, padx=10, pady=10)
#
# next_button = ttk.Button(self, text="Back",
#                          command=lambda: controller.show_frame(Page2))
# opt_button = ttk.Button(self, text="Optimal solution",
#
#                         command=lambda: controller.show_frame(Page2))
# next_button.grid(row=22, column=1, padx=10, pady=10)
# opt_button.grid(row=22, column=4, padx=10, pady=10)

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


app = tkinterApp()
app.mainloop()
