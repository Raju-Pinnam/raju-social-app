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


class Contact(models.Model):
    user_from = models.ForeignKey(User, related_name='rel_form_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"{self.user_from} follows {self.user_to}"


User.add_to_class('following',
                  models.ManyToManyField('self',
                                         through=Contact,
                                         related_name='followers',
                                         symmetrical=False))
