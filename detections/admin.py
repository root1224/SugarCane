"""Detection admin classes."""

# Django
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from django.contrib.auth.models import User

# Models
from detections.models import Detection
from detections.models import Note


class NoteInline(admin.TabularInline):
    model = Note
    verbose_name_plural = 'notes'


@admin.register(Detection)
class DetectionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False
    """Detection admin."""
    inlines =(NoteInline,)
    # Campos a mostrar
    list_display = ('pk','name','user','picture', 'picture_ndvi','picture_savi','picture_evi2','satatus_of_field','water_stress','water_stress_percent')
    change_links = ['user']

    # Linkear campos
    list_display_links = ('pk','name','satatus_of_field',)
    # Campos que se pueden buscar
    search_fields = (
    'user__username',
    'name',
    'satatus_of_field',
    )
    # Filtrar por campo
    list_filter =(
        'satatus_of_field',
        'created',
        'modified',
    )
