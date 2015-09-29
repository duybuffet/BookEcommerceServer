# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.encoding import smart_unicode

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Author(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_author'

    def __str__(self):
        return self.name

    def __unicode__(self):
        return smart_unicode(self.name)

class Book(models.Model):
    isbn = models.CharField(db_column='ISBN', unique=True, max_length=100, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cover_url = models.CharField(max_length=255, blank=True, null=True)
    price = models.FloatField()
    discount = models.FloatField(blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    num_pages = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_book'

    def __str__(self):
        if self.isbn.strip() != "":
            return self.isbn + " - " + self.title
        else:
            return self.title

    def __unicode__(self):
        return smart_unicode(self.title)


class BookAuthor(models.Model):
    author = models.ForeignKey(Author)
    book = models.ForeignKey(Book)

    class Meta:
        managed = False
        db_table = 'tbl_book_author'


class BookGenre(models.Model):
    book = models.ForeignKey(Book)
    genre = models.ForeignKey('Genre')

    class Meta:
        managed = False
        db_table = 'tbl_book_genre'


class Customer(models.Model):
    username = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=128, editable=False)
    fullname = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=45, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    ward = models.CharField(max_length=100, blank=True, null=True)
    street_number = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_customer'

    def __str__(self):
        return self.username + " - " + self.fullname

    def __unicode__(self):
        return smart_unicode(self.fullname)


class Genre(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'tbl_genre'

    def __str__(self):
        return self.name

    def __unicode__(self):
        return smart_unicode(self.name)

class OrderHistory(models.Model):
    STATUS_CHOICE = (
        (1, 'Waiting'),
        (2, 'Confirmed And Shipping'),
        (3, 'Completed'),
        (4, 'Cancel')
    )
    customer = models.ForeignKey(Customer, editable=False)
    staff = models.ForeignKey(AUTH_USER_MODEL)
    order_date = models.DateTimeField(blank=True, null=True)
    status = models.SmallIntegerField(blank=True, null=False, choices=STATUS_CHOICE, default=1)
    total = models.FloatField(blank=True, null=True)
    shipping_fee = models.FloatField(blank=True, null=True)
    shipping_address = models.TextField(blank=True, null=True)
    shipping_phone = models.CharField(max_length=45, blank=True, null=True)
    shipping_fullname = models.CharField(max_length=255, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_order_history'

    def fullname(self):
        return self.customer.fullname

    def __str__(self):
        return "#" + self.id + " - " + self.order_date

    def __unicode__(self):
        return smart_unicode(self.id)

class OrderLine(models.Model):
    book = models.ForeignKey(Book)
    order_history = models.ForeignKey(OrderHistory)
    quantity = models.IntegerField(blank=True, null=True)
    unit_price = models.FloatField(blank=True, null=True)
    discount = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_order_line'
