import os
import sys


book_path = "book/book.txt"  # расположения текстового файла с книгой
page_size = 1050  # кол-во символов на одной странице

book: dict[str, int] = {}


# возвращает строку с текстом страницы и ее размер
def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    punctuation_list = [',', '.', '!', ':', ';', '?']  # список символов на которые может быть окончен текст страницы
    



# ф-ция формирует словарь книги
def prepare_book(path: str) -> None:
    pass


# вызов функции prepare_book для подготовки текстового файла
prepare_book(os.path.join(sys.path[0], os.path.normpath(book_path)))

