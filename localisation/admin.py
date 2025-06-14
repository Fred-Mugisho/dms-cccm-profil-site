from django.contrib import admin
from .models import *

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['id', 'latitude', 'longitude', 'altitude', 'precision', 'created_at', 'updated_at']
    list_display_links = ['id', 'latitude', 'longitude', 'altitude', 'precision', 'created_at', 'updated_at']
    search_fields = ['id', 'latitude', 'longitude', 'altitude', 'precision', 'created_at', 'updated_at']
    list_filter = ['id', 'latitude', 'longitude', 'altitude', 'precision', 'created_at', 'updated_at']
    ordering = ['id', 'latitude', 'longitude', 'altitude', 'precision', 'created_at', 'updated_at']
    
@admin.register(Localisation)
class LocalisationAdmin(admin.ModelAdmin):
    list_display = ['nom', 'code', 'type', 'position__latitude', 'position__longitude', 'updated_at']
    search_fields = ['code', 'nom', 'type', 'position__latitude', 'position__longitude', 'updated_at']
    list_filter = ['type']
    ordering = ['type', 'id']
