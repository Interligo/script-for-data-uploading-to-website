from django.contrib import admin

from .models import Psychotherapist


@admin.register(Psychotherapist)
class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'methods', 'airtable_id')
    list_filter = ('name', 'airtable_id')
    search_fields = ('name', 'methods', 'airtable_id')
