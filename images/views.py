from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.conf import settings

from images.forms import ImageCreateForm
from images.models import Image

from common.decorators import ajax_required

from actions.utils import create_action

# import redis

# r = redis.Redis(host=settings.REDIS_HOST,
# port=settings.REDIS_PORT,
# db=settings.REDIS_DB)


@login_required
def image_create(req):

    if req.method == 'POST':
        form = ImageCreateForm(data=req.POST)

        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = req.user
            new_item.save()
            create_action(req.user, 'bookmarked image', new_item)

            messages.success(req, 'Image added successfuly')

            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm(data=req.GET)

    return render(req, 'images/image/create.html', {'section': 'images', 'form': form})


@login_required
def image_detail(req, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    total_views = r.incr(f'image:{image.id}:views')
    # r.zincrby('image_ranking', 1, image.id)

    return render(req, 'images/image/detail.html', {'section': 'images', 'image': image, 'total_views': total_views})


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
                create_action(req.user, 'likes', image)
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


# @login_required
# def image_ranking(req):

#     image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
#     image_ranking_ids = [int(id) for id in image_ranking]

#     most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
#     most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))

#     return render(req, 'images/image/ranking.html', {'section': 'images', 'most_viewed': most_viewed})
