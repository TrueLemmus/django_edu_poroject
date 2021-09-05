from users.models import User
from admin_panel.forms import UserAdminRegistrationForm, UserAdminProfileForm
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


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
