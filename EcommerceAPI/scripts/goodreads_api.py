import oauth2 as oauth
import time
import urlparse
import xml.etree.ElementTree as ET

__author__ = 'Duy'


url = 'http://www.goodreads.com'
request_token_url = '%s/oauth/request_token' % url
authorize_url = '%s/oauth/authorize' % url
access_token_url = '%s/oauth/access_token' % url
NONE_SEMENTIC_SHELVES = ['to-read','read','currently-reading','books-i-own','owned-books', 'favorites', 'ya', 'favorite']
key = '9ZzEFHzs9LwIdA3qt0fMw'
key_secret = 'e0UPVFymvpt261pfTMFvsE7NgD1Djpqp2WGclGmAEA'

def get_client():
    consumer = oauth.Consumer(key=key,
                              secret=key_secret)
    client = oauth.Client(consumer)
    response, content = client.request(request_token_url, 'GET')
    if response['status'] != '200':
        raise Exception('Invalid response: %s, content: ' % response['status'] + content)

    request_token = dict(urlparse.parse_qsl(content))

    authorize_link = '%s?oauth_token=%s' % (authorize_url,
                                            request_token['oauth_token'])
    print "Use a browser to visit this link and accept your application:"
    print authorize_link
    accepted = 'n'
    while accepted.lower() == 'n':
        # you need to access the authorize_link via a browser,
        # and proceed to manually authorize the consumer
        accepted = raw_input('Have you authorized me? (y/n) ')

    token = oauth.Token(request_token['oauth_token'],
                        request_token['oauth_token_secret'])

    client = oauth.Client(consumer, token)
    response, content = client.request(access_token_url, 'POST')
    if response['status'] != '200':
        raise Exception('Invalid response: %s' % response['status'])

    access_token = dict(urlparse.parse_qsl(content))

    # this is the token you should save for future uses
    print 'Save this for later: '
    print 'oauth token key:    ' + access_token['oauth_token']
    print 'oauth token secret: ' + access_token['oauth_token_secret']

    token = oauth.Token(access_token['oauth_token'],
                        access_token['oauth_token_secret'])

    return oauth.Client(consumer, token)

client = get_client()

def get_auth_user_id():
    response, content = client.request('%s/api/auth_user' % url,'GET')
    if response['status'] != '200':
        raise Exception('Cannot fetch resource: %s' % response['status'])

    root = ET.fromstring(content)
    return str(root[1].get('id'))


def get_user_friends(auth_user_id):
    list_friend = []
    response, content = client.request('%s/friend/user/%s?format=xml' % (url, auth_user_id), 'GET')
    if response['status'] != '200':
        raise Exception('Cannot fetch resource: %s' % response['status'])

    root = ET.fromstring(content)
    [list_friend.append(user[0].text) for user in root[1]]
    return list_friend


def get_user_books(auth_user_id):
    list_book = []
    response, content = client.request('%s/review/list.xml?v=2&id=%s&shelf=all' % (url, auth_user_id), 'GET')
    if response['status'] != '200':
        # raise Exception('Cannot fetch resource: %s' % response['status'])
        pass


    root = ET.fromstring(content)
    for review in root[1]:
        list_shelf = []
        [list_shelf.append(shelf.get('name')) if shelf.get('name') not in NONE_SEMENTIC_SHELVES else list_shelf for shelf in review[6]]
        list_book.append({"book_id" : review[1][0].text, "list_shelf" : list_shelf})
    return list_book


def get_user_book_shelves(auth_user_id, book_id):
    list_shelf = []
    response, content = client.request('%s/review/list.xml?v=2&id=%s&shelf=all' % (url, auth_user_id), 'GET')
    if response['status'] != '200':
        raise Exception('Cannot fetch resource: %s' % response['status'])

    root = ET.fromstring(content)
    for review in root[1]:
        if book_id == review[1][0].text:
            [list_shelf.append(shelf.get('name')) for shelf in review[6]]
    return list_shelf


def get_shelves_of_user(id):
    list_shelves = []
    response, content = client.request('%s/shelf/list.xml?user_id=%skey=%s' % (url, id, key), 'GET')
    if response['status'] != '200':
        pass

    root = ET.fromstring(content)
    for shelf in root[1]:
        name = shelf[1].text.lower()
        if name not in NONE_SEMENTIC_SHELVES : list_shelves.append(name)

    return list_shelves


def get_friends_books(list_friend):
    list_friends_books = []
    for friend_id in list_friend:
        response, content = client.request('%s/review/list.xml?v=2&id=%s&shelf=all' % (url, friend_id), 'GET')
        if response['status'] != '200':
            raise Exception('Cannot fetch resource: %s' % response['status'])
        root = ET.fromstring(content)
        list_book = []
        for review in root[1]:
            list_shelf = []
            [list_shelf.append(shelf.get('name')) for shelf in review[6]]
            list_book.append({review[1][0].text : list_shelf})
        list_friends_books.append({friend_id : list_book})
    return list_friends_books


def get_shelves_of_book_on_cloud(id):
    list_shelf = []
    response, content = client.request('%s/book/show/%s?format=xml&key=%s' % (url, id, key), 'GET')
    if response['status'] != '200':
        # raise Exception('Cannot fetch resource: %s' % response['status'])
        pass

    try:
        root = ET.fromstring(content)
        for shelf in root[1][26]:
            name = shelf.get('name').lower()
            if name not in NONE_SEMENTIC_SHELVES:
                list_shelf.append(name)
    except:
        pass
    return list_shelf

start = time.clock()
# print get_shelves_of_book_on_cloud(631932)
# user_id = get_auth_user_id()
# print get_user_books(user_id)
# print(get_friends_books(get_user_friends(user_id)))
# print get_shelves_of_book_on_cloud(55)
# print get_shelves_of_user(46199325)
print "Spending time : %s" % (time.clock() - start)