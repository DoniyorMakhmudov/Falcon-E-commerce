import django_ckeditor_5
from django.contrib import admin
from django.urls import path, include
from root.settings import STATIC_ROOT, MEDIA_ROOT, MEDIA_URL, STATIC_URL
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('apps.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
] + static(MEDIA_URL, document_root=MEDIA_ROOT) + static(STATIC_URL, document_root=STATIC_ROOT)
