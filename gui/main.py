import tkinter as tk
import sys
sys.path.append('../../')

from tkinter import ttk
from typing import Tuple, List
from gui.enter_parameters_page import ParametersEntryPage
from gui.utils import GameParameterStorage

LARGE_FONT = ("Raster Fonts", 24, '')
MIDDLE_FONT = ("Raster Fonts", 18, '')
SMALL_FONT = ("Raster Fonts", 12, '')

width = 2000
height = 1500

blue_color = 'blue3'
yellow_color = 'yellow'

class TkinterApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry('700x850+400+100')
        self.resizable(True, True)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        params = {
            'max_day': 'Amount of days under control',
            'first_sunday': 'Number of the first Sunday',
            'day_ship1_arrival': 'Day the first ship arrived',
            'day_ship2_arrival': 'Day the second ship arrived',
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

        for PageLayout in [StartPage, ParametersEntryPage]:
            # вызываем конструктор каждой из страниц
            frame = PageLayout(self.container, self)
            frame.grid(row=0, column=0, sticky='nsew')
            self.frames[PageLayout] = frame

        self.show_frame(StartPage)

    def show_frame(self, frame_to_show):
        frame = self.frames[frame_to_show]
        frame.tkraise()

    def get_parameters(self) -> List[GameParameterStorage]:
        return list(self.parameters.values())


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background=blue_color)
        label = tk.Label(
            self,
            text="HARBOUR STORE MANAGEMENT",
            font=LARGE_FONT,
            foreground=yellow_color,
            background=blue_color,
        )
        label.grid(
            row=0,
            column=0,
        )

        with open('gui/intro.txt', 'r') as file:
            intro = file.read()

        intro_label = tk.Label(
            self,
            text=intro,
            font=SMALL_FONT,
            foreground=yellow_color,
            background=blue_color,
            anchor='w',
            justify='left'
        )
        intro_label.grid(
            row=1,
            column=0,
            padx=10,
            pady=10,
        )

        enter_the_data = tk.Button(
            self,
            text="Enter the data",
            command=lambda: controller.show_frame(ParametersEntryPage),
            activebackground=blue_color,
            highlightbackground=blue_color,
            background=blue_color,
        )
        enter_the_data.grid(
            row=2,
            column=0,
        )


app = TkinterApp()
app.mainloop()
