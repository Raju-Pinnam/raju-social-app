from django.contrib import admin
from django.utils.html import format_html

from .models import Profile


@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        if object.photo:
            img_str = f"<img src='{object.photo.url}' width='50'/>"
        else:
            img_str = f'No image'
        return format_html(img_str)

    thumbnail.short_description = 'Profile Image'
    list_display = ['id', 'thumbnail', 'user', 'date_of_birth']
    search_fields = ['user', 'id']
    list_display_links = ['id', 'thumbnail', 'user']
    raw_id_fields = ['user', ]