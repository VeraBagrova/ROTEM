import tkinter as tk


class GameParameterStorage:
    """
    Класс для хранения одного параметра игры.
    name: название параметра аналогично параметрам в нодах;
    description: текстовое описание парметра, показываем его пользователю при вводе;
    intro_text: Label для отображения description'a
    user_entry: Entry для ввода пользовательского значения
    error_label: Label для отображения сообщения об ошибке валидации параметра
    optimal_solution: Label для отображения оптимального решения
    """
    def __init__(self,
                 name: str,
                 description: str,
                 intro_text: tk.Label = None,
                 user_entry: tk.Entry = None,
                 error_label: tk.Label = None,
                 optimal_solution: tk.Label = None):
        self.name = name
        self.description = description
        self.intro_text = intro_text
        self.user_entry = user_entry
        self.error_label = error_label
        self.optimal_solution = optimal_solution

        self.final_value = None


def check_input(entry, label):
    try:
        value = int(entry.get())
        if value < 2 or value > 14:
            label.config(text="Число должно быть от 2 до 14", fg="red")
        else:
            label.config(text="")
            return value
    except ValueError:
        label.config(text="Введите корректное число", fg="red")