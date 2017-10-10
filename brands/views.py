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
    response.set_cookie('_gaa', 'GA1.2.1050151658.150761992')
    return response


def results(request):
    return HttpResponse('asdf')
