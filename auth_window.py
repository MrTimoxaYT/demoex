import tkinter as tk
from tkinter import messagebox
from db_connection import connect_to_db
from table_window import TableWindow


class AuthWindow:
    """Окно авторизации."""

    def __init__(self, root):
        self.root = root
        self.root.title("Авторизация")

        frame = tk.Frame(root)
        frame.pack(padx=20, pady=20)

        tk.Label(frame, text="Логин").pack(anchor="w", pady=5)
        self.login_entry = tk.Entry(frame)
        self.login_entry.pack(fill="x", pady=5)

        tk.Label(frame, text="Пароль").pack(anchor="w", pady=5)
        self.password_entry = tk.Entry(frame, show="*")
        self.password_entry.pack(fill="x", pady=5)

        tk.Button(frame, text="Войти", command=self.authenticate).pack(pady=10)

    def authenticate(self):
        """Проверка логина и пароля."""
        login = self.login_entry.get()
        password = self.password_entry.get()

        if not login or not password:
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return

        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            query = "SELECT id FROM users WHERE login = %s AND passwd = %s"
            cursor.execute(query, (login, password))
            result = cursor.fetchone()
            connection.close()

            if result:
                user_id = result[0]
                self.root.destroy()
                TableWindow(user_id)
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль!")
