from mysql.connector import connect, Error
import os

environment = os.getenv('ENVIRONMENT', 'prod')

# Выбор конфигурации
if environment == 'test':
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


# Функция для вставки записи в таблице
def create_array(source_str, sorted_str):
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


def create_arrays(data):
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


# Функция для чтения из таблицы по имени
def get_by_limit(limit):
    try:
        with connect(**CONFIG) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT source_array FROM arrays LIMIT %s", (limit,))
            return cursor.fetchall()
    except Error as e:
        print(e)

    # # Функция для обновления записи в таблице по имени
    # def update_array_by_name(name, new_elements):
    #
    #     cursor.execute("UPDATE arrays SET elements = %s WHERE name = %s", (new_elements, name))
    #     connection.commit()
    #
    #
    # # Функция для удаления записи из таблицы по имени
    # def delete_array_by_name(name):
    #     cursor.execute("DELETE FROM arrays WHERE name = %s", (name,))
    #     connection.commit()


def clear_table():
    try:
        with connect(**CONFIG) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM arrays")
            connection.commit()
    except Error as e:
        print(e)
