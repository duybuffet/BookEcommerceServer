from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
import json
from scripts import database_query_utility as db
from scripts import helper as help
from EcommerceAPI.constants import *
from models import *
from EcommerceAPI.constants import *
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import datetime


def index(request):
    pass


def get_genres(request):
    if request.method == 'GET':
        data = db.get_all_genres()
        if len(data) > 0:
            return help.return_response(data, 200)
        else:
            data = {'error': 'Data not found'}
            return help.return_response(data, 404)
    else:
        data = {'error': 'Data not found'}
        return help.return_response(data, 404)


def get_books(request):
    if request.REQUEST.get('page'):
        page = int(request.REQUEST.get('page'))
    else:
        page = 1

    if request.method == 'GET':
        response_data = {}
        response_data['page'] = page
        response_data['max_page'] = 'False'
        books = db.get_all_book()
        response_data['books'] = books

        return help.return_response(response_data, 200)
    else:
        data = {'error': 'Data not found'}
        return help.return_response(data, 404)


def get_book_by_id(request):
    book_id = request.REQUEST.get('book_id')
    if request.method =='GET':
        book = db.get_book_by_id(book_id)
        return help.return_response(book, 200)
    else:
        data = {'error': 'Data not found'}
        return help.return_response(data, 404)


def get_books_by_genre(request):
    genre_id = request.GET.get("genre_id")
    if request.REQUEST.get('page'):
        page = int(request.REQUEST.get('page'))
    else:
        page = 1
    response_data = {}
    response_data['genre_id'] = genre_id
    response_data['max_page'] = 'False'
    books = []
    if request.method == 'GET':
        pages = Paginator(db.get_books_by_genre(genre_id), API_LIMIT_ELEMENT_PAGE)
        if page <= pages.num_pages and page > 0:
            books = pages.page(page).object_list
        else:
            response_data['max_page'] = 'True'
        # print data
        response_data['books'] = books
        return help.return_response(response_data, 200)
    else:
        data = {'error': 'Data not found'}
        return help.return_response(data, 404)


def get_new_books(request):
    if request.REQUEST.get('page'):
        page = int(request.REQUEST.get('page'))
    else:
        page = 1

    if request.method == 'GET':
        response_data = {}
        response_data['page'] = page
        response_data['max_page'] = 'False'
        books = []

        pages = Paginator(db.get_new_books(), API_LIMIT_ELEMENT_PAGE)
        if page <= pages.num_pages and page > 0:
            books = pages.page(page).object_list
        else:
            response_data['max_page'] = 'True'
        response_data['books'] = books
        return help.return_response(response_data, 200)
    else:
        data = {'error': 'Data not found'}
        return help.return_response(data, 404)


def search_book(request):
    key_word = request.REQUEST.get('key_word')
    search_type = request.REQUEST.get('search_type')
    if request.REQUEST.get('page'):
        page = int(request.REQUEST.get('page'))
    else:
        page = 1

    if request.method == 'GET':
        response_data = {}
        response_data['search_type'] = search_type
        response_data['page'] = page
        response_data['max_page'] = 'False'
        books = []
        if search_type == API_KEYWORD_SEARCH_TYPE_TITLE:
            pages = Paginator(db.get_books_by_title(key_word),API_LIMIT_ELEMENT_PAGE)
            if page <= pages.num_pages and page > 0:
                books = pages.page(page).object_list
            else:
                response_data['max_page'] = 'True'

            response_data['books'] = books
            return help.return_response(response_data, 200)
    else:
        data = {'error': 'Data not found'}
        return help.return_response(data, 404)


def get_books_by_recommendation(request):
    return HttpResponse(json.dumps({"success": "found"}), content_type='application/json', status=200)


def log_in(request):
    if request.method == 'POST':
        username = request.REQUEST.get('username')
        password = request.REQUEST.get('password')
        customer = Customer.objects.filter(username=username, password=password).values("id")
        if len(customer) == 1:
            customer = db.get_customer_by_id(customer[0]["id"])
            data = {'success': 'Login Successfully',
                    'customer_login': customer}
            return help.return_response(data, 200)
        else:
            data = {'error': 'Login failed'}
            return help.return_response(data, 404)
    else:
        data = {'error': 'Data not found'}
        return help.return_response(data, 404)


@csrf_exempt
def register(request):
    if request.method == 'POST':
        json_obj=json.loads(request.body)
        try:
            username = json_obj['username']
            password = json_obj['password']
            if len(Customer.objects.filter(username=username).values("id")) == 0:
                customer_new = Customer()
                customer_new.username = username
                customer_new.password = password
                customer_new.save()
                data = {'success': 'Register Successfully'}
                return help.return_response(data, 200)
            else:
                data = {'error': 'Username exist'}
                return help.return_response(data, 404)
        except Exception as inst:
            data = {'error': str(inst)}
            return help.return_response(data, 404)
    else:
        data = {'error': 'Data not found'}
        return help.return_response(data, 404)


def handle_profile(request):
    if request.method == 'GET':
        customer_id = request.REQUEST.get('customer_id')
        customer = db.get_customer_by_id(customer_id)
        return help.return_response(customer, 200)
    elif request.method == 'POST':
        customer_id = request.REQUEST.get('customer_id')
        customer_update = Customer.objects.get(pk=customer_id)
        if customer_update is None:
            data = {'error': 'Data not found'}
            return help.return_response(data, 404)
        else:
            try:
                customer_update.fullname = request.REQUEST.get('fullname')
                customer_update.city = request.REQUEST.get('city')
                customer_update.ward = request.REQUEST.get('ward')
                customer_update.email = request.REQUEST.get('email')
                customer_update.phone = request.REQUEST.get('phone')
                customer_update.street_number = request.REQUEST.get('street_number')
                customer_update.district = request.REQUEST.get('district')
                customer_update.postal_code = request.REQUEST.get('postal_code')
                customer_update.save()
                data = {'Success': 'Change profile successfully!'}
                return help.return_response(data, 200)
            except:
                data = {'error': 'Change profile failed'}
                return help.return_response(data, 404)
    else:
        data = {'error': 'Data not found'}
        return help.return_response(data, 404)


@csrf_exempt
def handle_order(request):
    if request.method == 'GET':
        order_id = request.REQUEST.get('order_id')
        order = db.get_order_by_id(order_id)
        return help.return_response(order, 200)
    elif request.method == 'POST':
        res = add_order(request)
        if res == True:
            json_obj=json.loads(request.body)
            data = {'success': 'Add order successfully'}
            return help.return_response(data, 200)
        else:
            data = {'error': 'Add order failed'}
            return help.return_response(data, 404)
    else:
        data = {'error': 'Data not found'}
        return help.return_response(data, 404)


def add_order(request):
    try:
        json_obj=json.loads(request.body)
        order = OrderHistory()
        order.status = ORDER_STATUS_WAITING
        order.customer = Customer.objects.get(id=json_obj['customer_id'])
        order.shipping_address = json_obj['shipping_address']
        order.shipping_fullname = json_obj['shipping_fullname']
        order.shipping_phone = json_obj['shipping_phone']
        order.total = json_obj['total']
        order.note = json_obj['note']
        order.order_date = datetime.datetime.now()
        order.save()
        order_id = order.id
        for line in json_obj['list_item']:
            order_line = OrderLine()
            order_line.quantity = line['quantity']
            order_line.unit_price = line['unit_price']
            order_line.discount = line['discount']
            order_line.book = Book.objects.get(pk=line['book_id'])
            order_line.order_history = OrderHistory.objects.get(pk=order_id)
            order_line.save()
        return True
    except Exception:
        return False


def get_orders_by_customer(request):
    if request.method == 'GET':
        data = db.get_orders_by_customer(request.REQUEST.get('customer_id'))
        return help.return_response(data, 200)
    else:
        data = {'error': 'Data not found'}
        return help.return_response(data, 404)
