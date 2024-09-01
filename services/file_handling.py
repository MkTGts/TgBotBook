import os
import sys


book_path = "book/book.txt"  # расположения текстового файла с книгой
page_size = 1050  # кол-во символов на одной странице

book: dict[str, int] = {}


# возвращает строку с текстом страницы и ее размер
def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    punctuation_list = [',', '.', '!', ':', ';', '?']  # список символов на которые может быть окончен текст страницы

    # проверка что первый символ след. страницы не из знаков пунктуации
    while text[size] in punctuation_list:
        size -= 1

    end_max = start + size  # максимально допустимый индекс последнего символа
    all_symbols = text[start:end_max]  # все символы в максимально допустимом диапозоне

    page = ''

    # обрез строки до символа пунктуцации
    for i in all_symbols[::-1]:
        if i in punctuation_list:  # если сивол из списка символоов пунктуации
            page = all_symbols[:all_symbols.rfind(i) + 1]  # обрезаем строку до этого символа
            break 

    return (page, len(page))
   

# ф-ция формирует словарь книги
def prepare_book(path: str) -> None:
    # достает текст из файла
    with open(path, "r", encoding="utf-8") as file:
        text = file.read()
    
    pg = 1  # инициализация счетчика страниц
    start = 0  # инициализация индекса позиции в тексте

    # проходится по тексту и разделяет его на страницы
    while start < len(text):  # пока стартовое значение меньше длины текста
        pg += 1  # прибавляет к счетчику страниц
        text_to_page = _get_part_text(text=text, start=start, size=page_size)  # достаем текст предназначенный для данной страницы
        book[pg] = text_to_page[0].strip()  # записываем текст странциы в словарь книги
        start += int(text_to_page[1]) + 1  # стартово значение увеличивается на уже пройденные индексы
        

# вызов функции prepare_book для подготовки текстового файла
prepare_book(os.path.join(sys.path[0], os.path.normpath(book_path)))










