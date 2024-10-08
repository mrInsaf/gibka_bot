import os
import sqlite3
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "gibka.db")
print(f'db_path is {db_path}')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


def select(query):
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.commit()
        return rows
    except Exception as e:
        print(f' yooo cheto pzc {e}')



def insert(table_name: str, data_list: list, auto_increment_id: int = 1):
    # Получаем информацию о столбцах в таблице
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [column[1] for column in cursor.fetchall()]
    columns = columns[auto_increment_id:]
    # print(columns)

    # Генерируем SQL-запрос для вставки данных
    placeholders = ', '.join(['?'] * len(columns))
    query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

    # Вставляем данные в таблицу
    cursor.execute(query, data_list)
    row_id = cursor.lastrowid
    conn.commit()
    return row_id


def select_products():
    return select(f"select * from products")


def select_modifications_by_product_id(product_id: int, ):
    return select(f"select * from modifications where product_id = {product_id}")


def select_modification_by_id(product_id: int, modification_id: int):
    return select(
        f"select * from modifications "
        f"where product_id = {product_id} "
        f"and id = {modification_id}"
    )
