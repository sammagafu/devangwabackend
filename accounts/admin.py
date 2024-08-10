from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'full_name', 'phonenumber', 'is_staff', 'is_active', 'is_individual', 'is_company')
    list_filter = ('is_staff', 'is_active', 'is_individual', 'is_company')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('full_name', 'phonenumber')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_active', 'is_individual', 'is_company', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'phonenumber', 'password1', 'password2', 'is_individual', 'is_company', 'is_staff', 'is_active'),
        }),
    )
    search_fields = ('email', 'full_name', 'phonenumber')
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(CustomUser, CustomUserAdmin)
