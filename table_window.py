import tkinter as tk
from tkinter import messagebox, ttk
from db_connection import connect_to_db
from add_order_window import AddOrderWindow


class TableWindow:
    """Окно для работы с таблицей заказов."""

    def __init__(self, user_id):
        self.user_id = user_id
        self.root = tk.Tk()
        self.root.title("Работа с таблицей заказов")

        # Верхняя часть с таблицей
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True)

        self.table = ttk.Treeview(table_frame, columns=("ID", "Название", "Стоимость"), show="headings")
        self.table.heading("ID", text="ID")
        self.table.heading("Название", text="Название")
        self.table.heading("Стоимость", text="Стоимость")
        self.table.pack(fill="both", expand=True, pady=10)

        self.load_orders()

        # Нижняя часть с кнопками
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Добавить заказ", command=self.add_order).pack(side="left", padx=10)
        tk.Button(button_frame, text="Удалить заказ", command=self.delete_order).pack(side="left", padx=10)

        self.root.mainloop()

    def load_orders(self):
        """Загрузка заказов из базы данных."""
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            query = "SELECT id, o_name, o_cost FROM orders WHERE uid = %s"
            cursor.execute(query, (self.user_id,))
            for row in cursor.fetchall():
                self.table.insert("", tk.END, values=row)
            connection.close()

    def add_order(self):
        """Добавление нового заказа."""
        AddOrderWindow(self.user_id, self.load_orders)

    def delete_order(self):
        """Удаление выбранного заказа."""
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите заказ для удаления!")
            return

        order_id = self.table.item(selected_item, "values")[0]
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            query = "DELETE FROM orders WHERE id = %s"
            cursor.execute(query, (order_id,))
            connection.commit()
            connection.close()
            self.table.delete(selected_item)
