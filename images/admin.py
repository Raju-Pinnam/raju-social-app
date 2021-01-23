from django.contrib import admin
from django.utils.html import format_html

from .models import Image


@admin.register(Image)
class ImageModelAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        img = f"<img src='{object.image.url}' width='70'/>"
        return format_html(img)

    list_display = ['id', 'thumbnail', 'title', 'user', 'slug', 'created']
    list_filter = ['created', 'user']
    search_fields = ['title', 'user', 'description']
    raw_id_fields = ['user']
    list_display_links = ['id', 'thumbnail', 'title', 'user', ]
