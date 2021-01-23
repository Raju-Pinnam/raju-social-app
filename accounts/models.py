from django.db import models
from django.contrib.auth import get_user_model

from .utils import profile_image_upload_path

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to=profile_image_upload_path, blank=True)

    def __str__(self):
        return f"Profile of User {self.user.username}"
