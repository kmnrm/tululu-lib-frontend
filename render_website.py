import json
from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)


def on_reload():
    template = env.get_template('template.html')
    rendered_page = template.render(books=books, books_pairs=books_pairs)
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


class Book(object):
    def __init__(self, book_path, image_path, title, author):
        self.book_path = book_path
        self.image_path = image_path
        self.title = title
        self.author = author


with open('books.json', 'r', encoding='utf-8') as my_file:
    parsed_books = my_file.read()
parsed_books = json.loads(parsed_books)

books = [
    Book(
        '/'.join(map(str, book["book_path"].split('\\')[-2:])),
        '/'.join(map(str, book["image_src"].split('\\')[-2:])),
        book["title"],
        book["author"]
    )
    for book in parsed_books
]

books_pairs = list(chunked(books, 2))

on_reload()

server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')
