import tkinter as tk
from tkinter import messagebox
from db_connection import connect_to_db


class AddOrderWindow:
    """Окно для добавления нового заказа."""

    def __init__(self, user_id, refresh_callback):
        self.user_id = user_id
        self.refresh_callback = refresh_callback
        self.window = tk.Toplevel()
        self.window.title("Добавить заказ")

        frame = tk.Frame(self.window)
        frame.pack(padx=20, pady=20)

        tk.Label(frame, text="Название").pack(anchor="w", pady=5)
        self.name_entry = tk.Entry(frame)
        self.name_entry.pack(fill="x", pady=5)

        tk.Label(frame, text="Стоимость").pack(anchor="w", pady=5)
        self.cost_entry = tk.Entry(frame)
        self.cost_entry.pack(fill="x", pady=5)

        tk.Button(frame, text="Добавить", command=self.add_order).pack(pady=10)

    def add_order(self):
        """Добавление нового заказа в базу данных."""
        name = self.name_entry.get()
        cost = self.cost_entry.get()

        if not name or not cost:
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return

        try:
            cost = int(cost)
        except ValueError:
            messagebox.showerror("Ошибка", "Стоимость должна быть числом!")
            return

        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            query = "INSERT INTO orders (o_name, o_cost, uid) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, cost, self.user_id))
            connection.commit()
            connection.close()
            messagebox.showinfo("Успех", "Заказ добавлен!")
            self.refresh_callback()
            self.window.destroy()
