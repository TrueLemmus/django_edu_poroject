from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models import F, Q
from products.models import ProductCategory
from users.models import User
from admin_panel.forms import UserAdminRegistrationForm, UserAdminProfileForm, ProductCategoryEditForm
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import connection


class MainView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'is_staff'

    def get(self, request, *args, **kwargs):
        context = {'title': 'GeekShop - Admin'}
        return render(request, 'admin_panel/index.html', context)


# Read
class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    template_name = 'admin_panel/admin-users.html'
    permission_required = 'is_staff'

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Админ | Пользователи'
        return context


# Create
class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = User
    template_name = 'admin_panel/admin-users-create.html'
    form_class = UserAdminRegistrationForm
    success_url = reverse_lazy('admin_panel:admin_users')
    permission_required = 'is_staff'

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Админ | Создать'
        return context


# Update
class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    template_name = 'admin_panel/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admin_panel:admin_users')
    permission_required = 'is_staff'

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Админ | Редактировать'
        return context


# Delete
class UserDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = User
    template_name = 'admin_panel/admin-users-update-delete.html'
    success_url = reverse_lazy('admin_panel:admin_users')
    permission_required = 'is_staff'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.safe_delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(UserDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Админ | Удалить'
        return context


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)


class ProductCategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ProductCategory
    template_name = 'admin_panel/product-category-update.html'
    form_class = ProductCategoryEditForm
    success_url = reverse_lazy('admin_panel:index')
    permission_required = 'is_staff'

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Админ | Редактирование категории'
        return context
