from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView

from apps.forms import CustomUserCreationForm, CustomAuthenticationForm
from apps.models import Product, CustomCategory, User


class MainTemplateView(TemplateView):
    template_name = 'apps/index.html'


# PRODUCTS
class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'apps/product/product-list.html'
    context_object_name = 'products'
    paginate_by = 3


# AUTH
class RegisterView(CreateView):
    template_name = 'apps/auth/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login_page')

    def form_valid(self, form):
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'apps/auth/login.html'
    authentication_form = CustomAuthenticationForm

    def get_success_url(self):
        return resolve_url('main_page')

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())


class CustomUserView(LoginRequiredMixin, CreateView):
    model = User
    template_name = 'apps/user/settings.html'
    fields = ['background_image', 'image', 'first_name',
              'last_name', 'email', 'phone_number', 'heading', 'introduction']
    success_url = reverse_lazy('settings_page')

    def form_valid(self, form):
        return super().form_valid(form)
