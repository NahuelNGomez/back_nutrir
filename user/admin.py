from attr import fields
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, PermissionManager, Permission
from .models import UsuarioPersonalizado
# Register your models here.

class UsuarioPersonalizadoAdmin(UserAdmin):

    model = UsuarioPersonalizado
    list_display = ('cuil', 'email', 'first_name','last_name')
    list_filter = ('groups',)
    fieldsets = (
        (None, {'fields': ('cuil', 'password', 'email', 'first_name', 'last_name', 'genero')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Permisos', {'fields': ('groups',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('cuil', 'password1', 'password2', 'email', 'first_name', 'last_name', 'genero', 'is_staff', 'is_active','groups',)}
        ),
    )
    search_fields = ('cuil','last_name')
    ordering = ('cuil',)

admin.site.register(UsuarioPersonalizado,UsuarioPersonalizadoAdmin)
admin.site.register(Permission)
