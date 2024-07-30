from django.urls import path

from apps.views import MainTemplateView, ProductListView, RegisterView, CustomLoginView, CustomUserView

urlpatterns = [
    path('', MainTemplateView.as_view(), name='main_page'),
    path('products', ProductListView.as_view(), name='product_list_page'),

    # auth
    path('register/', RegisterView.as_view(), name='register_page'),
    path('login/', CustomLoginView.as_view(), name='login_page'),


    # user
    path('settings/', CustomUserView.as_view(), name='settings_page')

]
