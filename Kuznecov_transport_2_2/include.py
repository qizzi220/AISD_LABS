# kuznetsov-lab2-transport-2-3
from dataclasses import dataclass  # Исправлено: dataclasses
from datetime import datetime, date, timedelta, time
from typing import Any, TypeVar, Generic
import ctypes
import base64
from Kuznecov_transport_2_2.route_exceptions import *


@dataclass
class BusStation:
    """ Датакласс busstation - реализация типа данных "остановка"
    """
    name: str
    coordinates: dict
    time_arrive: time
    time_departure: time

    def __repr__(self) -> str:
        return f"Остановка '{self.name}' (координаты: {self.coordinates})"

class BusRoute:

    """ Класс <автобусный маршрут> с реализацией всех заданий
    """

    def __init__(self) -> None:
        #собственная длина маршрута
        self._n = 0
        #собственная емкость массива,чтобы каждый раз ее увеличивать
        self._capacity = 1
        #сам массив ,созданные с помощью ctypes (базовый массив из C)
        self._A = self._make_array(self._capacity)

    def __len__(self) -> int:
        return self._n

    def _make_array(self, c: int):
        #использование библиотеки ctypes для создания привычного массива из C
        return (c * ctypes.py_object)()

    def _resize(self, new_cap: int) -> None:
        new_mas = self._make_array(new_cap)

        for i in range(self._n):
            new_mas[i] = self._A[i]

        self._A = new_mas
        self._capacity = new_cap

    def append(self, item: Any) -> None:
        #функция добавления в конец массив элемента со сложностью O(1) и в редких случая O(n)
        if self._n == self._capacity:
            self._resize(self._capacity * 2)

        self._A[self._n] = item
        self._n += 1

    def __getitem__(self, index: int) -> Any:
        # реализация magic метода __getitem__ ,который как раз таки возвращает элемент по индексу
        if 0 <= index < self._n:
            return self._A[index]
        raise RouteBoundsError(index, self._n)

    def __setitem__(self, index: int, value: Any) -> None:

        # реализация magic метода __setitem__, который устанавливает значение элемента значению

        if not 0 <= index < self._n:
            raise RouteBoundsError(index, self._n)
        self._A[index] = value

    def __contains__(self, item: Any) -> bool:
        # реализация magic метода __contains__ ,который отвечает за "value" IN "data" сахар
        for i in range(self._n):
            if self._A[i] == item:
                return True
        return False

    def __iter__(self):
        # создание итерируемого объекта
        for i in range(self._n):
            yield self._A[i]

    def __str__(self) -> str:
        # строковое представление объекта для print(data)
        elems = [str(self._A[i]) for i in range(self._n)]
        return f"[{', '.join(elems)}]"

    # --- Перегрузка операторов ---

    def __add__(self, other: 'BusRoute') -> 'BusRoute':
        # magic метод для сложения двух классов busroute типа busroute1 + busroute2
        new_route = BusRoute()

        for item in self:
            new_route.append(item)

        for item in other:
            new_route.append(item)
        return new_route

    def __mul__(self, times: int) -> 'BusRoute':
        # magic метод для умножения типа busroute * 2

        if not isinstance(times, int):
            return NotImplemented

        new_route = BusRoute()
        if times <= 0:
            return new_route

        for _ in range(times):
            for item in self:
                new_route.append(item)
        return new_route

    def get_next_stop(self, current_index: int) -> BusStation:
        #метод нахождения следующей остановки, вызываем кастомные исключения. Просто берем индекс текущей  + 1
        if self._n == 0:
            raise EmptyRouteError()

        if current_index >= self._n - 1:
            raise EndOfRouteError()

        return self[current_index + 1]

    def get_stop_after_n(self, current_index: int, n: int) -> BusStation:
        #метод реализации нахождения остановки через n остановок. Просто берем cur_ind + n
        if self._n == 0:
            raise EmptyRouteError()

        target_index = current_index + n

        if target_index >= self._n:
            raise EndOfRouteError(f"Через {n} остановок автобус уже сойдет с маршрута.")

        return self[target_index]

    def build_reverse_route(self) -> 'BusRoute':
        #Построение реверсивного маршрута с помощь слайсов в питоне. Также можно реализовать и без слайсов
        new_route = BusRoute()
        for i in range(self._n - 1, -1, -1):
            new_route.append(self._A[i])
        return new_route

    def __reversed__(self):
        #магический метод,реализующий .reversed() метод
        for i in range(self._n - 1, -1, -1):
            yield self._A[i]

    def total_route_time(self):
        #метод,возвращающий полное время в пути маршрута. Для этого импортируем datetime библиотеку из питона
        if self._n < 2:
            return "0:00:00" # если всего одна остановка, то маршрут пустой -> время в маршруте 0

        start = self._A[0].time_departure
        end = self._A[self._n - 1].time_arrive

        dt_start = datetime.combine(date.today(), start) #для нормализации данных,нужно вызывать метод combine и комбинировать данные с сегодняшней датой
        dt_end = datetime.combine(date.today(), end) #для нормализации данных,нужно вызывать метод combine и комбинировать данные с сегодняшней датой

        if dt_end < dt_start:
            dt_end += timedelta(days=1)

        return dt_end - dt_start

    def save_rout_report(self, filename="route_report.txt"):
        with open(filename, "w", encoding="utf-8") as f:
            f.write("=" * 60 + "\n")
            f.write(f"{'ПОДРОБНЫЙ ОТЧЕТ ПО МАРШРУТУ':^60}\n")
            f.write("=" * 60 + "\n\n")

            f.write(f"Количество остановок: {self._n}\n")
            f.write(f"Общее время в пути:  {self.total_route_time()}\n")
            f.write("-" * 60 + "\n")

            header = f"{'Название остановки':<25} | {'Прибытие':^12} | {'Отправление':^12}\n"
            f.write(header)
            f.write("-" * 60 + "\n")

            for stop in self:
                row = (f"{stop.name:<25} | "
                       f"{stop.time_arrive.strftime('%H:%M'):^12} | "
                       f"{stop.time_departure.strftime('%H:%M'):^12}\n")
                f.write(row)

            f.write("-" * 60 + "\n")
            f.write(f"Отчет сформирован: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

        print(f"Отчет успешно сохранен в файл {filename}")

    def print_route_asmd(self):
        #формируем md строку с помощью f-строки
        header = f"{'Название остановки':<25} | {'Прибытие':^12} | {'Отправление':^12}"
        print(header)
        print("-" * 60)

        for stop in self:
            row = (f"{stop.name:<25} | "
                   f"{stop.time_arrive.strftime('%H:%M'):^12} | "
                   f"{stop.time_departure.strftime('%H:%M'):^12}")
            print(row)
        print("-" * 60)

    def save_route_base64(self, filename="route_base64.txt"):
        """сохранение маршрута, где КАЖДАЯ строка закодирована в Base64"""
        with open(filename, "w", encoding="utf-8") as f:
            for stop in self:
                # Формируем информацию только об одной остановке
                row_text = (f"{stop.name} | "
                            f"{stop.time_arrive.strftime('%H:%M')} | "
                            f"{stop.time_departure.strftime('%H:%M')}")

                b64_bytes = base64.b64encode(row_text.encode('utf-8'))
                b64_string = b64_bytes.decode('utf-8')

                f.write(b64_string + "\n")

        print(f"Base64-маршрут сохранен в {filename}")

    def get_stops_within_time(self, start_index: int, limit_minutes: int):
        """нахождение остановок через какое-то время. Тут также требуется нормализация времени,тк datetime не умеет работать с просто минутами и секундами, а только с датами"""
        limit = timedelta(minutes=limit_minutes)
        total_spent = timedelta(minutes=0)
        results = []

        for i in range(start_index, self._n - 1):
            current_stop = self[i]
            next_stop = self[i + 1]

            d1 = datetime.combine(date.today(), current_stop.time_departure)
            d2 = datetime.combine(date.today(), next_stop.time_arrive)

            # обработка полночи для кольцевого маршрута

            if d2 < d1:
                d2 += timedelta(days=1)

            travel_time = d2 - d1
            total_spent += travel_time

            if total_spent <= limit:
                results.append(next_stop)
            else:
                break
        return results


class CircleBusRoute(BusRoute):
    def __getitem__(self, index: int) -> Any:
        """перегрузка метода для кольцевого маршрута с помощью super()"""
        if self._n == 0:
            raise EmptyRouteError()

        circular_index = index % self._n
        return super().__getitem__(circular_index)

    def __str__(self) -> str:
        """аналогичная перегрузка для строкового представления"""
        base_str = super().__str__()
        return f"Кольцевой маршрут: {base_str}"

    def iter_infinite(self):
        """бесконечно ходит по кругу"""
        while self._n > 0:

            for stop in super().__iter__():
                yield stop

    def get_next_stop(self, current_index: int) -> BusStation:
        if self._n == 0:
            raise EmptyRouteError()

        next_index = (current_index + 1) % self._n
        return super().__getitem__(next_index)