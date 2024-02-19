import os
import random
import time
import unittest

import config.environment as environment
import sort

environment.setTest()

import repo

# Функция для генерации массива
def generate_random_array():
    size = random.randint(5, 20)
    return [random.randint(0, 50) for _ in range(size)]


# Генерация массивов заданного количества и добавление в бд
def insert_test(num_arrays):
    start_time = current_milli_time()
    data_to_insert = [
        ((','.join(map(str, generate_random_array()))), 'NULL')
        for _ in range(num_arrays)
    ]

    repo.insert_arrays(data_to_insert)

    end_time = current_milli_time()
    elapsed_time = minus_round_num(end_time, start_time)

    return elapsed_time


# Сортировка 100 случайных массивов из бд
def sort_random_test():
    start_time = current_milli_time()
    sum_time = 0

    arrays = repo.get_by_limit(100)
    for row in arrays:
        array = list(map(int, row[0].split(',')))

        start_time_in = current_milli_time()

        sort.heap_sort(array)

        end_time_in = current_milli_time()
        sum_time += minus_round_num(end_time_in, start_time_in)

    end_time = current_milli_time()
    elapsed_time = minus_round_num(end_time, start_time)

    return elapsed_time, (sum_time / 100)


def clear_table_test():
    start_time = current_milli_time()

    repo.clear_table()

    end_time = current_milli_time()
    elapsed_time = minus_round_num(end_time, start_time)

    return elapsed_time


def minus_round_num(num1, num2):
    return num1 - num2


def current_milli_time():
    return round(time.time() * 1000)


class Test(unittest.TestCase):
    os.environ['ENVIRONMENT'] = 'tests'

    @classmethod
    def setUpClass(cls):
        repo.create_mysql_db()
        repo.create_table()

    # Сортировка заданных массивов
    def test_sort(self):
        array_test1 = [12, 11, 13, 5, 6, 7, 3, 23, 13, 15]
        array_test2 = [1, 2, 98, 1, 2, 55, 5, 3, 13, 198, 43, 42, 32]

        array_check1 = [3, 5, 6, 7, 11, 12, 13, 13, 15, 23]
        array_check2 = [1, 1, 2, 2, 3, 5, 13, 32, 42, 43, 55, 98, 198]

        sort.heap_sort(array_test1)
        sort.heap_sort(array_test2)

        self.assertEqual(array_test1, array_check1)
        self.assertEqual(array_test2, array_check2)

    # Сортировка 100 / 1000 / 10000 сгенерированных массивов и сохранение в БД
    def test_insert_100(self):
        num_arrays_1 = 100
        time_1 = insert_test(num_arrays_1)
        print(
            f"Test 1: Inserting {num_arrays_1} "
            f"arrays took {time_1} ms"
        )
        elapsed_time, average_time = sort_random_test()
        print(
            f"Test 1.4: Took {elapsed_time} ms, "
            f"average time {average_time} ms"
        )
        clear_time = clear_table_test()
        print(f"Test 1.5: Clear table took {clear_time} ms")

    def test_insert_1000(self):
        num_arrays_2 = 1000
        time_2 = insert_test(num_arrays_2)
        print(
            f"Test 2: Inserting {num_arrays_2} "
            f"arrays took {time_2} ms"
        )
        elapsed_time, average_time = sort_random_test()
        print(
            f"Test 2.4: Took {elapsed_time} ms,  "
            f"average time {average_time} ms"
        )
        clear_time = clear_table_test()
        print(f"Test 2.5: Clear table took {clear_time} ms")

    def test_insert_10000(self):
        num_arrays_3 = 10000
        time_3 = insert_test(num_arrays_3)
        print(
            f"Test 3: Inserting {num_arrays_3} "
            f"arrays took {time_3} ms"
        )
        elapsed_time, average_time = sort_random_test()
        print(
            f"Test 3.4: Took {elapsed_time},  "
            f"average time {average_time} ms"
        )
        clear_time = clear_table_test()
        print(f"Test 3.5: Clear table took {clear_time} ms")
