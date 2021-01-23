from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ImageCreationForm
from .models import Image


@login_required
def image_create(request):
    if request.method == "POST":
        form = ImageCreationForm(data=request.POST)
        print("Is coming to POST")
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False, user=request.user)
            new_item.user = request.user
            new_item.save()
            messages.success(request, "Image created")
            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreationForm(data=request.GET)
    context = {
        'section': 'images',
        'form': form
    }
    return render(request, 'images/image/create.html', context)


def image_detail(request, img_id=None, slug=None):
    image = get_object_or_404(Image, id=img_id, slug=slug)
    context = {
        'section': 'images',
        'image': image
    }
    return render(request, 'images/image/detail.html', context)