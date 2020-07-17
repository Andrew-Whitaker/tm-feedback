from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import User
from .forms import SignUpForm, MyUserChangeForm


class MyUserAdmin(UserAdmin):
    add_form = SignUpForm
    form = MyUserChangeForm
    model = User
    list_display = ['username', ]
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ()}),
    )


admin.site.register(User, MyUserAdmin)
