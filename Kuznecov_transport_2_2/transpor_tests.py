import unittest
from datetime import time

from Kuznecov_transport_2_2.include import BusRoute, BusStation, CircleBusRoute
from Kuznecov_transport_2_2.route_exceptions import EmptyRouteError, RouteBoundsError, EndOfRouteError


class TestTransportSystem(unittest.TestCase):

    def setUp(self):
        """создаем тестовые данные для тестов"""
        self.route = BusRoute()

        self.stop1 = BusStation("пупкино", {"x": 0, "y": 1}, time(10, 0), time(10, 5))
        self.stop2 = BusStation("село молочное", {"x": 228, "y": 1488}, time(10, 10), time(10, 32))
        self.stop3 = BusStation("сиксевен", {"x": 67, "y": 42}, time(11, 0), time(11, 20))

    def test_append_and_len(self):
        """проверяем базовое добавление"""
        self.assertEqual(len(self.route), 0)
        self.route.append(self.stop1)
        self.route.append(self.stop2)
        self.assertEqual(len(self.route), 2)
        self.assertEqual(self.route[0].name, "пупкино")

    def test_total_time_midnight(self):
        """Проверяем крайний случай прохода через полночь"""
        night_stop1 = BusStation("ночное_пупкино", {"x": 101, "y": 111}, time(23, 0), time(23, 30))
        night_stop2 = BusStation("ночной_сиксеве", {"x": 10, "y": 11}, time(0, 30), time(0, 45))

        self.route.append(night_stop1)
        self.route.append(night_stop2)

        total = self.route.total_route_time()
        self.assertEqual(total.total_seconds(), 3600)

    def test_exceptions_raised(self):
        """тест ошибок"""
        # тест ошибки пустого маршрута
        with self.assertRaises(EmptyRouteError):
            self.route.get_next_stop(0)

        # сделали маршрут непустым для проверки следующих ошибок
        self.route.append(self.stop1)

        # проверка обращению к несуществующему индексу
        with self.assertRaises(RouteBoundsError):
            _ = self.route[5]

        # проверка запроса следующей остановки, когда мы на последней
        with self.assertRaises(EndOfRouteError):
            self.route.get_next_stop(0)

    def test_circle_route_logic(self):
        """проверяем фишку кольцевого маршрута (остаток от деления)"""
        circle = CircleBusRoute()
        circle.append(self.stop1)
        circle.append(self.stop2)

        # Запрашиваем индекс 1 (это stop2). Следующей должна быть stop1 (индекс 0)
        next_stop = circle.get_next_stop(1)
        #проверяем имя "пупкино"
        self.assertEqual(next_stop.name, "пупкино")

    def test_reversed_route(self):
        """проверка построения обратного маршрута"""
        self.route.append(self.stop1)
        self.route.append(self.stop2)

        # Строим обратный маршрут
        rev_route = self.route.build_reverse_route()

        # Нулевой элемент перевернутого = последний элемент оригинального
        self.assertEqual(rev_route[0].name, "село молочное")
        self.assertEqual(rev_route[1].name, "пупкино")


if __name__ == '__main__':
    unittest.main()