from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario
from .forms import CustomUsuarioCreateForm, CustomUsuarioChangeForm

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    add_form = CustomUsuarioCreateForm
    form = CustomUsuarioChangeForm
    model = Usuario
    list_display = ['email','first_name', 'last_name', 'is_staff']
    readonly_fields = ['last_login', 'date_joined']
    fieldsets = (
        ('Login', {'fields':('email', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'telefone', 'cpf')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')})
    )