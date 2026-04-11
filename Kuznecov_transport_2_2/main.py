import base64
from datetime import time
import os

from Kuznecov_transport_2_2.include import BusRoute, BusStation, CircleBusRoute


def main():
    print("=== ЗАПУСК СИСТЕМЫ УПРАВЛЕНИЯ МАРШРУТАМИ ===\n")

    # 1. создаем остановки
    stop1 = BusStation("МАГНИТОГОРСК", {"x": 50.1, "y": 30.2}, time(8, 0), time(8, 10))
    stop2 = BusStation("сиксеве", {"x": 50.5, "y": 30.8}, time(8, 25), time(8, 30))
    stop3 = BusStation("село молочное", {"x": 51.0, "y": 31.0}, time(8, 45), time(8, 50))
    stop4 = BusStation("ГАЗАН", {"x": 51.5, "y": 31.5}, time(9, 10), time(9, 20))

    # 2. создаем маршрут и добавляем остановки
    route = BusRoute()
    route.append(stop1)
    route.append(stop2)
    route.append(stop3)
    route.append(stop4)

    # 3. демонстрация вывода в консоль
    print("1. ВЫВОД МАРШРУТА В ВИДЕ ТАБЛИЦЫ:")
    route.print_route_asmd()
    print()

    # 4. демонстрация логических функций
    print("2. ДЕМОНСТРАЦИЯ ЛОГИКИ МАРШРУТА:")
    print(f"-> Общее время в пути: {route.total_route_time()}")

    # где будем через 2 остановки, если мы сейчас на Автовокзале?
    future_stop = route.get_stop_after_n(0, 2)
    print(f"-> Через 2 остановки от МАГНИТОГОРСКА будет: {future_stop.name}")

    # куда успеем доехать за 40 минут от Автовокзала?
    reachable_stops = route.get_stops_within_time(0, 40)
    names = [s.name for s in reachable_stops]
    print(f"-> За 40 минут от МАГНИТОГОРСКА мы доедем до: {', '.join(names)}\n")

    # 5. демонстрация сохранения отчетов
    print("3. ГЕНЕРАЦИЯ ОТЧЕТОВ И СОХРАНЕНИЕ В ФАЙЛЫ:")

    report_file = "my_route_report.txt"
    base64_file = "my_route_base64.txt"

    route.save_rout_report(report_file)
    route.save_route_base64(base64_file)

    # 6. проверка Base64
    print("\n4. ПРОВЕРКА РАБОТОСПОСОБНОСТИ BASE64:")
    if os.path.exists(base64_file):
        with open(base64_file, "r", encoding="utf-8") as f:
            # читаем первую закодированную строчку
            encoded_lines = f.readlines()
            for i in encoded_lines:
                print(f"Закодированная строка из файла:\n{i}")
                # декодируем обратно
                decoded_bytes = base64.b64decode(i)
                decoded_str = decoded_bytes.decode('utf-8')
                print(f"Расшифрованный результат:\n{decoded_str}\n")

    # 7. демонстрация кольцевого маршрута
    print("\n5. ДЕМОНСТРАЦИЯ КОЛЬЦЕВОГО МАРШРУТА:")
    circle_route = CircleBusRoute()
    circle_route.append(stop1)
    circle_route.append(stop2)
    print(f"Создан кольцевой маршрут длиной {len(circle_route)} остановки.")
    print(f"Текущая остановка (индекс 1): {circle_route[1].name}")
    print(f"Следующая остановка (индекс 2): {circle_route.get_next_stop(1).name} (Маршрут пошел по кругу!)")


if __name__ == '__main__':
    main()