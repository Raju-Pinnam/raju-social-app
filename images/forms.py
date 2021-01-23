from django import forms
from django.utils.text import slugify
from django.core.files.base import ContentFile

from urllib import request

from a_social_project.utils import get_random_str

from .models import Image


class ImageCreationForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'url', 'description']
        widgets = {
            'url': forms.HiddenInput,
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError("have to enter JPEG URLS only")
        return url

    def save(self, force_insert=False, force_update=False, commit=True, *args, **kwargs):
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(self.cleaned_data['title'])
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f"{name}-{get_random_str(size=5)}.{extension}"
        response = request.urlopen(image_url)
        user = kwargs.get('user' or None)
        if user is not None:
            image.user = user
        image.image.save(image_name, ContentFile(response.read()), save=False)
        if commit:
            image.save()
        return image
