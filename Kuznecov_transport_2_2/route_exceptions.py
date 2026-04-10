class BusRouteError(Exception):
    pass

class EmptyRouteError(BusRouteError):
    def __init__(self, message= "Маршрут пуст!"):
        super().__init__(message)

class RouteBoundsError(BusRouteError):
    def __init__(self, index, size):
        super().__init__(f"Остановка с индексом {index} не существует. Всего в маршруте {size} остановок.")

class EndOfRouteError(BusRouteError):
    def __init__(self, message = "Данная остановка является конечной. Маршрут окончен!"):
        super().__init__(message)