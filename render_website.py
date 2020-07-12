import os
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
    os.makedirs('pages', exist_ok=True)
    for page_num, page_books_pairs in enumerate(books_pairs_split):
        rendered_page = template.render(
            books=books,
            books_pairs=page_books_pairs,
            pages=pages_quantity,
            current_page=page_num + 1
        )
        with open(f'pages/index{page_num + 1}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


class Book(object):
    def __init__(self, book_path, image_path, title, author, genres):
        self.book_path = book_path
        self.image_path = image_path
        self.title = title
        self.author = author
        self.genres = genres


with open('books.json', 'r', encoding='utf-8') as my_file:
    parsed_books = my_file.read()
parsed_books = json.loads(parsed_books)

books = [
    Book(
        '../{path}'.format(
            path='/'.join(map(str, book["book_path"].split('\\')[-2:]))
        ),
        '../{path}'.format(
            path='/'.join(map(str, book["image_src"].split('\\')[-2:]))
        ),
        book["title"],
        book["author"],
        book["genres"]
    )
    for book in parsed_books
]

pairs_divider = 10
books_pairs = list(chunked(books, 2))
books_pairs_split = list(chunked(books_pairs, pairs_divider))
pages_quantity = len(books_pairs_split)

on_reload()

server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')
