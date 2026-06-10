import random
import string


class UrlShortener:
    def __init__(self):
        # основной словарь: короткий код -> длинная ссылка
        self.links = {}
        # словарь для 2-го варианта: длинная ссылка -> короткий код
        # нужно, чтобы хранить историю сокращенных ссылок
        self.reverse_links = {}

    def _generate_code(self):
        # генерирует рандомную строку из 5 символов (буквы + цифры)
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(5))

    def add_link(self, long_url):
        # ВАРИАТИВНАЯ ЧАСТЬ 2
        # проверяем, существует ли уже такая длинная ссылка
        if long_url in self.reverse_links:
            return self.reverse_links[long_url]

        # если ссылки нет, создаем новый код
        short_code = self._generate_code()

        # на случай коллизии (если такой короткий код рандомно уже сгенерировался)
        while short_code in self.links:
            short_code = self._generate_code()

        # сохраняем в оба словаря
        self.links[short_code] = long_url
        self.reverse_links[long_url] = short_code

        return short_code

    def get_long_link(self, short_code):
        # возвращает длинную ссылку или None, если кода нет
        return self.links.get(short_code)

    def is_code_exists(self, short_code):
        return short_code in self.links

    def print_all(self):
        if not self.links:
            print("База ссылок пуста.")
            return

        for code, url in self.links.items():
            print(f"{code} -> {url}")



if __name__ == "__main__":
    shortener = UrlShortener()

    print("--- обязательная часть ---")
    url1 = "https://example.com/articles/python-basics"
    code1 = shortener.add_link(url1)
    print(f"добавлена ссылка: {url1}")
    print(f"получен код: {code1}")

    print(f"\nпроверка существования кода '{code1}': {shortener.is_code_exists(code1)}")
    print(f"получение ссылки по коду: {shortener.get_long_link(code1)}")

    print("\n--- Вариативная часть 2 ---")
    print("пробуем добавить ту же самую длинную ссылку еще раз...")
    code2 = shortener.add_link(url1)
    print(f"получен код: {code2}")

    if code1 == code2:
        print("cистема вернула старый код вместо создания нового.")

    print("\n--- пывод всех ссылок ---")
    shortener.add_link("https://vk.com/im")
    shortener.add_link("https://github.com")
    shortener.print_all()