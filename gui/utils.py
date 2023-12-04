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