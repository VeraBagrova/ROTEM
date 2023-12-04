import tkinter as tk
from tkinter import ttk

LARGEFONT = ("Times New Roman", 24, '')
MIDDLEFONT = ("Times New Roman", 18, '')
SMALLFONT = ("Times New Roman", 12, '')


class tkinterApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self, width=600, height=600)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, EnterTheDataPage, Page2):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='dark blue')
        label = ttk.Label(
            self,
            text="HARBOUR STORE MANAGEMENT",
            font=LARGEFONT,
            foreground='yellow',
            background='dark blue'
        )
        label.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            columnspan=2,
        )

        with open('intro.txt', 'r') as file:
            intro = file.read()

        intro_label = ttk.Label(
            self,
            text=intro,
            font=SMALLFONT,
            width=100,
            foreground='yellow',
            background='dark blue'
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
            command=lambda: controller.show_frame(EnterTheDataPage)
        )
        enter_the_data.grid(
            row=2,
            column=0,
            padx=10,
            pady=10
        )


# second window frame page1
class EnterTheDataPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='black')

        # for i in range(12):
        #     for j in range(6):
        #         # Create entry cell with some text inside
        #         entry = tk.Entry(self, width=10)
        #         entry.insert(tk.END, f"Row {i}, Column {j}")
        #         entry.grid(row=4 + i, column=j, padx=10, pady=10)

        entry = tk.Entry(self, width=40, foreground='black', background='turquoise')
        entry.insert(tk.END, f"Day (Sunday Red) ")
        entry.grid(row=0, column=0, padx=2)

        entry = tk.Entry(self, width=40, background='dark blue', foreground='white')
        entry.insert(tk.END, "Storing mass at the end should be equal or more than ")
        entry.grid(row=1, column=0, padx=2)

        entry = tk.Entry(self, width=40, foreground='black', background='turquoise')
        entry.insert(tk.END, "Ship 1 mass at the end should be equal to  ")
        entry.grid(row=2, column=0, padx=2)

        entry = tk.Entry(self, width=40, background='dark blue', foreground='white')
        entry.insert(tk.END, "Ship 2 mass at the end should be equal to  ")
        entry.grid(row=3, column=0, padx=2)

        entry = tk.Entry(self, width=40, foreground='black', background='turquoise')
        entry.insert(tk.END, "Day load to ship 1 left and right limits: ")
        entry.grid(row=4, column=0, padx=2)

        entry = tk.Entry(self, width=40, background='dark blue', foreground='white')
        entry.insert(tk.END, "Day load to ship 2 left and right limits: ")
        entry.grid(row=5, column=0, padx=2)

        entry = tk.Entry(self, width=40, foreground='black', background='turquoise')
        entry.insert(tk.END, "Penalty for ship1 unloading ")
        entry.grid(row=6, column=0, padx=2)

        for i in range(7):
            for j in range(6):
                # Create entry cell with some text inside
                if i % 2 == 0:
                    entry = tk.Entry(self, width=15, foreground='black', background='turquoise')
                else:
                    entry = tk.Entry(self, width=15, foreground='white', background='dark blue')

                entry.insert(tk.END, f" ")
                entry.grid(row=i, column=1 + j, padx=2)

        next_button = ttk.Button(
            self,
            text="Back",
            command=lambda: controller.show_frame(Page2)
        )
        opt_button = ttk.Button(
            self,
            text="Optimal solution",
            command=lambda: controller.show_frame(Page2)
        )
        next_button.grid(row=7, column=1, columnspan=2, pady=12)
        opt_button.grid(row=7, column=4, columnspan=2, pady=12)
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


# third window frame page2
class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page 2", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="Page 1",
                             command=lambda: controller.show_frame(IntroPage))

        # putting the button in its place by
        # using grid
        button1.grid(row=1, column=1, padx=10, pady=10)

        # button to show frame 3 with text
        # layout3
        button2 = ttk.Button(self, text="Startpage",
                             command=lambda: controller.show_frame(StartPage))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=1, padx=10, pady=10)


# Driver Code
app = tkinterApp()
app.mainloop()
