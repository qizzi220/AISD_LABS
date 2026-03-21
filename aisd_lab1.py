import time
import random
import tracemalloc
import pandas as pd

def count_even(arr):
    count = 0
    for x in arr:
        if x % 2 == 0:
            count += 1
    return count

def generate_array(n):
    arr = []
    for i in range(n):
        arr.append(random.randint(0, 10**6))
    return arr

def measure_time(func, data):
    start = time.perf_counter()
    start_memory = tracemalloc.start()
    func(data)
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    end_memory = tracemalloc.stop()
    return f"{end - start} байтов_памяти_затрачено:{peak}"

def find_item(item, array: list):
    for i in array:
        if i == item:
            return True
    return False

def find_premax(array: list):
    max1, max2 = array[0], array[0]
    for i in array:
        if i > max1:
            max1, max2 = i, max1
        elif i > max2:
            max2 = i
    return max2


def binary_search(item: int, array: list) -> int:
    l = 0
    r = len(array) - 1

    while l <= r:
        mid = l + (r - l) // 2

        if array[mid] == item:
            return mid

        if array[mid] < item:
            l = mid + 1
        else:
            r = mid - 1

    return -1

def times_table(n: int):
    for i in range(1, n + 1):
        row = []
        for j in range(1, n + 1):
            row.append((i) * j)
        print(*row, end='\n')
    return f"Таблица {n} чисел"


def insertion_sort(arr, left, right):
    #Сортировка вставками для маленьких фрагментов.
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def merge(arr, l, m, r):
    #Слияние двух отсортированных частей внутри исходного массива.
    len1, len2 = m - l + 1, r - m
    left, right = [], []
    for i in range(0, len1):
        left.append(arr[l + i])
    for i in range(0, len2):
        right.append(arr[m + 1 + i])

    i, j, k = 0, 0, l

    while i < len1 and j < len2:
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1

    while i < len1:
        arr[k] = left[i]
        k += 1
        i += 1

    while j < len2:
        arr[k] = right[j]
        k += 1
        j += 1


def tim_sort(arr):
    n = len(arr)
    MIN_MERGE = 32  # Обычно берется от 32 до 64

    # 1. Сортируем отдельные подмассивы размером MIN_MERGE
    for start in range(0, n, MIN_MERGE):
        end = min(start + MIN_MERGE - 1, n - 1)
        insertion_sort(arr, start, end)

    # 2. Начинаем объединение отсортированных фрагментов
    size = MIN_MERGE
    while size < n:
        for left in range(0, n, 2 * size):
            # Находим середину и конец для слияния
            mid = min(n - 1, left + size - 1)
            right = min((left + 2 * size - 1), (n - 1))

            # Сливаем два подмассива, если они существуют
            if mid < right:
                merge(arr, left, mid, right)

        size *= 2


def render_table_to_md(df):
    # Заголовки
    cols = list(df.columns)
    header = "| " + " | ".join(cols) + " |"
    separator = "| " + " | ".join(["---"] * len(cols)) + " |"

    # Строки данных
    rows = []
    for _, row in df.iterrows():
        formatted_row = "| " + " | ".join(map(str, row.values)) + " |"
        rows.append(formatted_row)

    return "\n".join([header, separator] + rows)
if __name__ == '__main__':
    sizes = [100, 1000, 5000, 10000]
    results = []
    for n in sizes:
        arr = generate_array(n)
        t = measure_time(count_even, arr)
        print(n, t, end='\n')

        print(find_item(arr[random.randint(0, n)], arr), 'finditem', end='\n')

        print(find_premax(arr), 'premax', end='\n')

        print(binary_search(arr[random.randint(0, n)], arr), "binary_search", end='\n')

        algo_compl, space_compl = measure_time(tim_sort, arr).split()
        results.append({"N": n, 'сложность алгоритмическая': algo_compl,
        'сложность пространственная': space_compl})


results = pd.DataFrame(results)

#print(results)

markdown_table = render_table_to_md(results)

with open("README.md", "w", encoding="utf-8") as f:
    f.write("# Лабораторная работа №1\n\n")
    f.write("## Результаты замеров сложности\n\n")
    f.write(markdown_table)
    f.write("\n")


print(times_table(10))
#print(times_table(20))


