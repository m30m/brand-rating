from django.db.models import Avg
from django.db.models import Count
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Brand, BrandRating


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def vote(request):
    msg = ''
    if request.method == 'POST':
        if '_gaa' in request.COOKIES:
            msg = 'rep'
        else:
            brand_id = int(request.POST.get('brand-id'))
            rating = int(request.POST.get('rating'))
            brand = get_object_or_404(Brand, id=brand_id)
            brand_rating = BrandRating(brand=brand, rating=rating, ip=get_client_ip(request))
            brand_rating.save()
            msg = 'vote'
    response = render(request, 'vote.html', context={'brands': Brand.objects.all(), 'message': msg})
    if msg == 'vote':
        response.set_cookie('_gaa', 'GA1.2.1050151658.150761992')
    return response


def results(request):
    brand_img = {}
    for brand in Brand.objects.all():
        brand_img[brand.id] = brand.image.url
    brands_data = Brand.objects.values('id').annotate(avg_rating=Avg('brandrating__rating'),
                                                      rate_count=Count('brandrating')).order_by('-avg_rating')
    for brand in brands_data:
        brand['img'] = brand_img[brand['id']]
    return render(request, 'results.html', context={'brands': brands_data})
