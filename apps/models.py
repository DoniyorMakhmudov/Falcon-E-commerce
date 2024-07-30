from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Model, CharField, FloatField, ImageField, ForeignKey, CASCADE, PositiveSmallIntegerField, \
    IntegerField, ManyToManyField, DateTimeField, JSONField, PositiveIntegerField, CheckConstraint, SmallIntegerField, \
    SlugField, Q, TextField
from django.db.models.functions import Now
from django.utils.text import slugify
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django_ckeditor_5.fields import CKEditor5Field


class User(AbstractUser):
    background_image = ImageField(upload_to='background_image/', null=True, blank=True)
    image = ImageField(upload_to='users/', null=True, blank=True)
    carts = ManyToManyField('Product', through='Cart', through_fields=('user', 'product'), related_name='user_carts')
    phone_number = CharField(20, blank=True)
    heading = CharField(50, blank=True, null=True)
    introduction = TextField(blank=True, null=True)


class CustomCategory(MPTTModel):
    name = CharField(max_length=255)
    slug = SlugField(unique=True, editable=False)
    parent = TreeForeignKey('self', CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['name']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name)
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name


class Tag(Model):
    name = CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(Model):
    title = CharField(max_length=150)
    image = ImageField(upload_to='users/%Y/%m/%d/', blank=True, null=True)
    category = ForeignKey('CustomCategory', CASCADE)
    description = CKEditor5Field()
    specification = JSONField(default=dict, null=True, blank=True)
    price = FloatField(null=True, blank=True, help_text='price dollarda')
    discount = PositiveSmallIntegerField(default=0, help_text='Chegirma foizi')
    shipping_cost = IntegerField(null=True)
    quantity = IntegerField(null=True)
    tag = ManyToManyField(Tag)
    updated_at = DateTimeField(auto_now_add=True, db_default=Now())
    created_at = DateTimeField(auto_now=True, db_default=Now())

    @property
    def discounted_price(self):
        return self.price - (self.price * self.discount) // 100

    def __str__(self):
        return self.title


class Review(Model):
    title = CharField(max_length=255)
    product = ForeignKey('Product', CASCADE)
    author = ForeignKey('User', CASCADE)
    rating = SmallIntegerField(default=0)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            CheckConstraint(check=Q(rating__gte=0, rating__lte=10), name="rating_range_0_10"),
        ]


class ProductImage(Model):
    image = ImageField(upload_to='products/%Y/%m/%d/', blank=True)
    product = ForeignKey('apps.Product', CASCADE, related_name='images')
    created_at = DateTimeField(auto_now_add=True)


class Order(Model):
    user = ForeignKey('apps.User', CASCADE)
    created_at = DateTimeField(auto_now_add=True)


class Cart(Model):
    user = ForeignKey('apps.User', CASCADE, related_name='cart_products')
    product = ForeignKey('apps.Product', CASCADE, related_name='cart_users')
    created_at = DateTimeField(auto_now_add=True)


class OrderItem(Model):
    order = ForeignKey('Order', CASCADE)
    quantity = PositiveIntegerField(default=1, db_default=1)


class Region(Model):
    name = CharField(max_length=255)


class District(Model):
    name = CharField(max_length=255)
    region = ForeignKey('Region', CASCADE)


class Country(Model):
    name = CharField(max_length=255)
    code = CharField(max_length=5)
