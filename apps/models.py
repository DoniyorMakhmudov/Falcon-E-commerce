from django.db.models import Model, CharField, FloatField, ImageField, ForeignKey, CASCADE, PositiveSmallIntegerField, \
    IntegerField, ManyToManyField, DateTimeField, JSONField
from django.db.models.functions import Now


class Category(Model):
    name = CharField(max_length=40)

    def __str__(self):
        return self.name


class Tag(Model):
    name = CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(Model):
    title = CharField(max_length=150)
    image = ImageField(upload_to='users/%Y/%m/%d/')
    category = ForeignKey('apps.Category', CASCADE)
    description = JSONField(default=dict, null=True, blank=True)
    price = FloatField()
    discount = PositiveSmallIntegerField(default=0, help_text='Chegirma foizi')
    shipping_cost = IntegerField()
    quantity = IntegerField(null=True)
    tag = ManyToManyField(Tag)
    updated_at = DateTimeField(auto_now_add=True, db_default=Now())
    created_at = DateTimeField(auto_now=True, db_default=Now())

    @property
    def discounted_price(self):
        return self.price - (self.price * self.discount) // 100


