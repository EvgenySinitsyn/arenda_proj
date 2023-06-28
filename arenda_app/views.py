from django.db.models.functions import Coalesce
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import City, Space, SpaceImage
from .forms import SelectSpaces
from django.shortcuts import get_object_or_404


def get_side_objects():
    popular_spaces = Space.objects.all().order_by('-views')[:2]
    form = SelectSpaces()
    cities = City.objects.all()
    return popular_spaces, form, cities



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
    old_post = request.session.get('_old_post')
    if old_post:
        spaces = filter_spaces(spaces, old_post)
        request.session['_old_post'] = None
    if request.method == 'POST':
        spaces = filter_spaces(spaces, request.POST)
    popular_spaces, form, cities = get_side_objects()
    context = {'form': form,
               'cities': cities,
               'spaces': spaces,
               'popular_spaces': popular_spaces,
               }
    return render(request, template_name='arenda_app/index.html', context=context)


def space_detail(request, space_id):
    popular_spaces, form, cities = get_side_objects()
    if request.method == 'GET':
        space = get_object_or_404(Space, id=space_id)
    if request.method == 'POST':
        request.session['_old_post'] = request.POST
        return redirect('index')
    context = {'form': form,
               'cities': cities,
               'space': space,
               'images': space.images.all(),
               'popular_spaces': popular_spaces,
               }
    return render(request, template_name='arenda_app/single.html', context=context)
