from django.urls import path

from admin_panel.views import MainView, UserListView, UserCreateView, UserUpdateView, UserDeleteView

app_name = 'admin_panel'

urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('users/', UserListView.as_view(), name='admin_users'),
    path('users-create/', UserCreateView.as_view(), name='admin_users_create'),
    path('users-update/<int:pk>/', UserUpdateView.as_view(), name='admin_users_update'),
    path('users-delete/<int:pk>/', UserDeleteView.as_view(), name='admin_users_delete'),
]
