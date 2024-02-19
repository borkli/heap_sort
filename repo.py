from mysql.connector import connect, Error

from config.environment import ENVIRONMENT
from gui_main import Array

# Выбор конфигурации
if ENVIRONMENT == 'test':
    from config.config_test import CONFIG_INIT, CONFIG, DB_NAME
else:
    from config.config import CONFIG_INIT, CONFIG, DB_NAME


# Создание бд, если её нет
def create_mysql_db():
    try:
        with connect(**CONFIG_INIT) as connection:
            create_db_query = f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"
            with connection.cursor() as cursor:
                cursor.execute(create_db_query)
                connection.commit()
    except Error as e:
        print(e)


def create_table():
    try:
        with connect(**CONFIG) as connection:
            create_table = """
                CREATE TABLE IF NOT EXISTS arrays(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    source_array VARCHAR(255),
                    sorted_array VARCHAR(255)
                )
                """
            with connection.cursor() as cursor:
                cursor.execute(create_table)
                connection.commit()
    except Error as e:
        print(e)


# Функция для вставки записи в таблицу
def insert_array(source_str, sorted_str):
    try:
        with connect(**CONFIG) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO arrays (source_array, sorted_array) "
                "VALUES (%s, %s)",
                (source_str, sorted_str)
            )
            connection.commit()
    except Error as e:
        print(e)


# Вставка нескольких записей
def insert_arrays(data):
    try:
        with connect(**CONFIG) as connection:
            cursor = connection.cursor()
            cursor.executemany(
                "INSERT INTO arrays (source_array, sorted_array) "
                "VALUES (%s, %s)",
                data
            )
            connection.commit()
    except Error as e:
        print(e)


# Обновление массива по id
def update_array(array: Array):
    try:
        with connect(**CONFIG) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE arrays "
                "SET source_array = %s, sorted_array = %s "
                "WHERE id = %s",
                (array.source_array, array.sort_array, array.id)
            )
            connection.commit()
    except Error as e:
        print(e)


# Функция для чтения из таблицы с лимитом
def get_by_limit(limit):
    try:
        with connect(**CONFIG) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT source_array FROM arrays LIMIT %s", (limit,))
            return cursor.fetchall()
    except Error as e:
        print(e)


# Возвращает все массивы из БД
def get_arrays():
    try:
        with connect(**CONFIG) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM arrays")
            return cursor.fetchall()
    except Error as e:
        print(e)


def delete_array(id):
    try:
        with connect(**CONFIG) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM arrays WHERE id = %s", (id,))
            connection.commit()
    except Error as e:
        print(e)


# Удалить все записи в таблице
def clear_table():
    try:
        with connect(**CONFIG) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM arrays")
            connection.commit()
    except Error as e:
        print(e)
