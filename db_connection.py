import mysql.connector
from tkinter import messagebox

from config import *



def connect_to_db():
    """Подключение к базе данных."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        messagebox.showerror("Ошибка подключения", f"Не удалось подключиться к БД:\n{err}")
        return None