from django.contrib import admin

from .models import Action


@admin.register(Action)
class ActionModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'verb', 'target', 'created')
    list_filter = ('created',)
    search_fields = ('verb',)
    raw_id_fields = ('user', )
