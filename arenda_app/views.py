from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect
from .models import City, Space, SpaceImage
from .forms import SelectSpaces
from django.http import HttpResponse


def filter_spaces(spaces, post):
    spaces = spaces.filter(type_id=post['type'])
    spaces = spaces.filter(rent_type_id=post['rent_type'])
    spaces = spaces.filter(building__city__name=post['city'])
    if post['rent_type'] == '1':
        if post['price_from']:
            spaces = spaces.filter(day_price__gte=float(post['price_from']))
        if post['price_to']:
            spaces.filter(day_price__lte=float(post['price_to']))
    else:
        if post['price_from']:
            spaces = spaces.filter(month_price__gte=float(post['price_from']))
        if post['price_to']:
            spaces = spaces.filter(month_price__lte=float(post['price_to']))
    if post['area_from']:
        spaces = spaces.filter(area__gte=float(post['area_from']))
    if post['area_to']:
        spaces = spaces.filter(area__lte=float(post['area_to']))
    return spaces


def index(request):
    spaces = Space.objects.all().order_by('-views')
    popular_spaces = Space.objects.all().order_by('-views')[:2]
    if request.method == 'POST':
        spaces = filter_spaces(spaces, request.POST)
    form = SelectSpaces()
    cities = City.objects.all()

    photos = SpaceImage.objects.filter(space=1)
    context = {'form': form,
               'cities': cities,
               'spaces': spaces,
               'photos': photos,
               'popular_spaces': popular_spaces,
               }
    return render(request, template_name='arenda_app/index.html', context=context)


def show_spaces(request):
    old_post = request.session.get('_old_post')
    if old_post['rent_type'] == 'Посуточно':
        spaces = Space.objects.filter(hour_price__gte=old_post['price_from'])
    return HttpResponse(content=spaces[0].month_price)
