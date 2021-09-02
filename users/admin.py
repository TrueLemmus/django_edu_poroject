from baskets.admin import BasketAdmin
from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [BasketAdmin]
