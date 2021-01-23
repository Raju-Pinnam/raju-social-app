from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse

from a_social_project.utils import get_random_str

from .utils import image_upload_path

User = get_user_model()


class Image(models.Model):
    user = models.ForeignKey(User, related_name='images_created', on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to=image_upload_path)
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)
    users_like = models.ManyToManyField(User, related_name='images_liked', blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"{slugify(self.title)} {get_random_str(size=5)}"
            self.slug = slugify(self.slug)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])
