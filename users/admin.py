""" User admin classes """
# https://docs.djangoproject.com/en/3.1/ref/contrib/admin/

# Django
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from django.contrib.auth.models import User

# Models
from users.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """ Profile admin. """

    # Campos a mostrar
    list_display = ('pk','user', 'phone_number','picture','is_expert')

    # Linkear campos
    list_display_links = ('pk', 'user')

    # Campos que se pueden buscar
    search_fields = (
    'user__username',
    'user__last_name',
    'user__first_name',
    )

    # Filtrar por campo
    list_filter =(
        'is_expert',
        'user__is_staff',
        'modified',
    )

    # Formato del detalle de los perfiles
    fieldsets = (
        ('Profile',{
            'fields' : (('user','picture'),),
        }),
        ('Extra Info', {
            'fields' : (('phone_number', 'is_expert'),)
        }),
        ('Matadata',{
            'fields' : (('created','modified'),)
        }),
    )

    # Campos no editables
    readonly_fields = ('created', 'modified',)



class ProfileInline(admin.StackedInline):
    """ Profile in-line admin for users. """

    model = Profile
    can_delete = False
    verbose_name_plural = 'profiles'

class UserAdmin(BaseUserAdmin):
    """ Add profile admin to base user admin. """

    inlines = (ProfileInline,)
    list_display = (
    'username',
    'email',
    'first_name',
    'last_name',
    'is_active',
    'is_staff',
    'is_superuser',
    )

admin.site.unregister(User)  # Desregistar el modelo User
admin.site.register(User, UserAdmin)   # Registar el modelo y la clase de admin que vamos a utilizar
