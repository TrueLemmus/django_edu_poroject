from users.models import User
from admin_panel.forms import UserAdminRegistrationForm, UserAdminProfileForm
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse


@user_passes_test(lambda u: u.is_staff)
def index(request):
    context = {'title': 'GeekShop - Admin'}
    return render(request, 'admin_panel/index.html', context)


# Read
@user_passes_test(lambda u: u.is_staff)
def admin_users(request):
    context = {'title': 'GeekShop - Пользователи', 'users': User.objects.all()}
    return render(request, 'admin_panel/admin-users.html', context)


# Create
@user_passes_test(lambda u: u.is_staff)
def admin_users_create(request):
    if request.method == 'POST':
        form = UserAdminRegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_users'))
    else:
        form = UserAdminRegistrationForm()
    context = {'title': 'GeekShop - Создание пользователя', 'form': form}
    return render(request, 'admin_panel/admin-users-create.html', context)


# Update
@user_passes_test(lambda u: u.is_staff)
def admin_users_update(request, id):
    selected_user = User.objects.get(id=id)
    if request.method == 'POST':
        form = UserAdminProfileForm(instance=selected_user, files=request.FILES, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin_panel:admin_users'))
    else:
        form = UserAdminProfileForm(instance=selected_user)
    context = {
        'title': 'GeekShop - Редактирование пользователя',
        'selected_user': selected_user,
        'form': form,
    }
    return render(request, 'admin_panel/admin-users-update-delete.html', context)


# Delete
@user_passes_test(lambda u: u.is_staff)
def admin_users_delete(request, id):
    user = User.objects.get(id=id)
    user.safe_delete()
    return HttpResponseRedirect(reverse('admin_panel:admin_users'))
