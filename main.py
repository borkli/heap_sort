# 2. Пирамидальная сортировка / Heapsort

def heapify(arr, n, i):
    largest = i  # Инициализуем наибольший элемент как корень
    l = 2 * i + 1
    r = 2 * i + 2

    # Существует ли левый дочерний элемент больший, чем корень
    if l < n and arr[i] < arr[l]:
        largest = l

    # Существует ли правый дочерний элемент больший, чем корень
    if r < n and arr[largest] < arr[r]:
        largest = r

    # Заменяем корень, если нужно
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


# Функция для сортировки массива заданного размера
def heap_sort(arr):
    n = len(arr)

    # Построение max-heap.
    for i in range(n, -1, -1):
        heapify(arr, n, i)

    # Один за другим извлекаем элементы
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    return arr


if __name__ == '__main__':
    arr = [12, 11, 13, 5, 6, 7, 3, 23, 13, 15]
    arr = heap_sort(arr)
    n = len(arr)
    print("Sorted array is")
    for i in range(n):
        print("%d" % arr[i])
