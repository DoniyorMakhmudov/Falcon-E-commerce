from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from apps.models import Product, Tag, CustomCategory, Review, ProductImage


# Register your models here.
class ProductImageStackedInline(admin.StackedInline):
    model = ProductImage
    min_num = 0
    max_num = 5
    extra = 2


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    inlines = [ProductImageStackedInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(CustomCategory)
class CustomMPTTModelAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 20


@admin.register(Review)
class ReviewModelAdmin(admin.ModelAdmin):
    pass
