from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST

from images.forms import ImageCreateForm
from images.models import Image
from common.decorators import ajax_required


@login_required
def image_create(req):

    if req.method == 'POST':
        form = ImageCreateForm(data=req.POST)

        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            new_item.user = req.user
            new_item.save()

            messages.success(req, 'Image added successfuly')

            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm(data=req.GET)

    return render(req, 'images/image/create.html', {'section': 'images', 'form': form})


@login_required
def image_detail(req, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)

    return render(req, 'images/image/detail.html', {'section': 'images', 'image': image})


@ajax_required
@login_required
@require_POST
def image_like(req):
    image_id = req.POST.get('id')
    action = req.POST.get('action')

    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)

            if action == 'like':
                image.users_like.add(req.user)
            else:
                image.users_like.remove(req.user)

            return JsonResponse({'status': 'ok'})
        except:
            pass

    return JsonResponse({'status': 'error'})


@login_required
def image_list(req):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = req.GET.get('page')

    try:
        images = paginator.page(page)

    except PageNotAnInteger:
        images = paginator.page(1)

    except EmptyPage:

        if req.is_ajax():
            return HttpResponse('')

        images = paginator.page(paginator.num_pages)

    if req.is_ajax():
        return render(req, 'images/image/list_ajax.html', {'section': 'images', 'images': images})

    return render(req, 'images/image/list.html', {'section': 'images', 'images': images})
