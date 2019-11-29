from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('nickname', 'name', 'surname', 'email', 'phone')
    search_fields = ('email', 'phone')
    readonly_fields = ('date_joined',)
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('nickname', 'name', 'surname', 'phone')}),
        ('Permissions', {
            'fields': ('groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nickname','name','surname','email', 'phone', 'password1', 'password2'),
        }),
    )
