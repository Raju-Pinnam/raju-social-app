from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from common.decorators import ajax_required

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


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse()
        images = paginator.page(paginator.num_pages)
    context = {
        'section': 'images',
        'images': images,
    }
    if request.is_ajax():
        return render(request, 'images/image/list_ajax.html', context)
    return render(request, 'images/image/list.html', context)


def image_detail(request, img_id=None, slug=None):
    image = get_object_or_404(Image, id=img_id, slug=slug)
    context = {
        'section': 'images',
        'image': image
    }
    return render(request, 'images/image/detail.html', context)


@login_required
@require_POST
@ajax_required
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action').strip()
    print(image_id, action)
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
        except:
            pass
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})
