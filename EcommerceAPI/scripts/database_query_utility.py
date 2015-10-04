from django.core.wsgi import get_wsgi_application
from EcommerceAPI.models import Genre, BookGenre, Book, BookAuthor, Author, Customer, OrderHistory, OrderLine
from EcommerceAPI.constants import *
from django.db.models import Q, F
from django.db.models import Count
from django.db.models.functions import *
import os
import sys
import logging

parentdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, parentdir)

env = "BookEcommerce.settings"

# setup_environ(settings)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", env)

application = get_wsgi_application()

__author__ = 'duy'


# BOOK API

def get_all_genres():
    result = []
    genres = Genre.objects.all()
    for gen in genres:
        result.append({"id": gen.id, "name": gen.name})
    return result


def convert_cover(url):
    """
    convert url
    :param date: string
    :return:string
    """
    url = url.replace('\r','')
    url = url.replace('\n','')
    if url.endswith('.png'):
        url = "http://os-jpupacic-omis.skole.hr/upload/os-jpupacic-omis/images/static3/1241/Image/jpg_1666-boy-with-books-in-their-hands.jpg"
    return url


def get_new_books():
    """
    search book new limit 10
    :return: list object Book
    """
    filters = Q()
    books = Book.objects.filter(filters).order_by('id').reverse().values('id', 'title', 'cover_url', 'discount', 'stock')[:API_LIMIT_ELEMENT_SEARCH]
    list_book = []
    for book in books:
        data = {'id': book['id'], 'title': book['title'], 'cover_url': book['cover_url'], 'discount': book['discount'], 'stock': book['stock']}
        list_book.append(data)
    return list_book


def get_books_by_title(key_word):
    """
    search book by title book
    :param key_word: key word title
    :return:list object Book
    """
    filters = Q(title__contains = key_word)
    books = Book.objects.filter(filters).values('id', 'title')
    list_book = []
    for book in books:
        data = {'id': book['id'], 'title': book['title']}
        list_book.append(data)
    return list_book


def get_books_by_genre(genre_id):
    """
    Get list of books that have genre_id
    :param genre_id:
    :return: list books having genre_id
    """
    result = []
    try:
        list_book_id = BookGenre.objects.filter(genre_id = genre_id).values("book_id")
        list_book = Book.objects.filter(pk__in = list_book_id)
        for book in list_book:
            result.append({'id' : book.id, 'name' : book.title, 'cover_url' : convert_cover(book.cover_url),
                           'price' : book.price, 'stock' : book.stock, 'discount' : book['discount']})
        return result
    except Exception as inst:
        logging.error(type(inst))
        logging.error(inst)
        return []


def get_all_book():
    """
    get id and title of All book
    :return: list object book
    """
    filters = Q()
    books = Book.objects.filter(filters).values('id', 'title', 'cover_url', 'discount', 'stock')
    list_book = []
    for book in books:
        data = {'id': book['id'], 'title': book['title'], 'cover_url': book['cover_url'], 'discount': book['discount'], 'stock': book['stock']}
        list_book.append(data)
    return list_book


def get_book_by_id(book_id):
    list_author = []
    list_genre = []

    for genre in BookGenre.objects.filter(book__id=book_id).values("genre_id"):
        list_genre.append(Genre.objects.filter(id=genre['genre_id']).values("name")[0]["name"])

    for author in BookAuthor.objects.filter(book__id=book_id).values("author_id"):
        list_author.append(Author.objects.filter(id=author['author_id']).values("name")[0]["name"])

    filters = Q(id=book_id)
    book = Book.objects.filter(filters).values("id", "isbn",
                                               "cover_url", "title",
                                               "description", "price",
                                               "discount", "stock",
                                               "num_pages")
    data = {}
    if  len(book) > 0:
        data = {"id" : book[0]["id"], "cover_url": book[0]["cover_url"], "description": book[0]["description"],
                "discount": book[0]["discount"], "num_pages": book[0]["num_pages"], "stock": book[0]["stock"],
                "isbn": book[0]["isbn"], "title": book[0]["title"], "price": book[0]["price"],
                "author": list_author, "genre": list_genre}
    return data


# CUSTOMER API

def get_customer_by_id(customer_id):
    customer = Customer.objects.filter(id=customer_id).values("id", "fullname", "email", "phone",
                                                              "city", "district", "ward",
                                                              "street_number", "postal_code")
    if len(customer) > 0:
        data = {"id": customer[0]["id"], "fullname": customer[0]["fullname"], "email": customer[0]["email"],
                "phone": customer[0]["phone"], "city": customer[0]["city"], "district": customer[0]["district"],
                "ward": customer[0]["ward"], "street_number": customer[0]["street_number"],
                "postal_code": customer[0]["postal_code"]}
    return data


def get_order_by_id(order_id):
    list_item = []
    order_lines = OrderLine.objects.filter(order_history__id=order_id).values("book_id", "quantity")
    for line in order_lines:
        line_details = {"quantity": line["quantity"]}
        book = Book.objects.get(pk=line["book_id"])
        if book is None:
            line_details["title"] = ""
        else:
            line_details["title"] = book.title
        list_item.append(line_details)

    order = OrderHistory.objects.filter(pk=order_id).values("id", "status", "shipping_fee", "total", "order_date", "note")
    if len(order) > 0:
        data = {"id": order_id, "status": order[0]["status"], "shipping_fee": order[0]["shipping_fee"],
                "total": order[0]["total"], "order_date": unicode(order[0]["order_date"].strftime("%d/%m/%Y %H:%M:%S")),
                "list_item": list_item, "note": order[0]["note"]}
        return data
    return {}


def get_orders_by_customer(customer_id):
    orders = OrderHistory.objects.filter(customer__id=customer_id).values("id", "status", "total", "order_date").reverse()
    data = []
    for order in orders:
        data.append({"id": order["id"], "status": order["status"],
                "total": order["status"], "order_date": unicode(order["order_date"].strftime("%d/%m/%Y %H:%M:%S"))})
    result = {"orders": data}
    return result


# print get_orders_by_customer(1)