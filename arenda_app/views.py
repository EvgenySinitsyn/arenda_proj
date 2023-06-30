from django.shortcuts import render, redirect
from .models import City, Space, SpaceImage
from .forms import SelectSpaces
from django.shortcuts import get_object_or_404


PAGE_LIMIT = 8


def clear_post(request):
    request.session['_old_post'] = None
    return redirect('index')


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


def index(request, page=1):
    popular_spaces, form, cities = get_side_objects()
    spaces = Space.objects.all().order_by('-views')
    if request.method == 'POST':
        request.session['_old_post'] = request.POST
        return redirect('index')
    old_post = request.session.get('_old_post')
    if old_post:
        spaces = filter_spaces(spaces, old_post)
        form = SelectSpaces(old_post)

    page_spaces = spaces[(page-1) * PAGE_LIMIT:((page-1) * PAGE_LIMIT) + PAGE_LIMIT]
    page_count = len(spaces) // PAGE_LIMIT + 1
    context = {'form': form,
               'cities': cities,
               'spaces': page_spaces,
               'popular_spaces': popular_spaces,
               'page_count': range(1, page_count + 1),
               'pages_amount': page_count,
               'current_page': page,
               }
    return render(request, template_name='arenda_app/index.html', context=context)


def space_detail(request, space_id):
    popular_spaces, form, cities = get_side_objects()
    if request.method == 'GET':
        space = get_object_or_404(Space, id=space_id)
        space.views += 1
        space.save()

    context = {'form': form,
               'cities': cities,
               'space': space,
               'images': space.images.all(),
               'popular_spaces': popular_spaces,
               }
    return render(request, template_name='arenda_app/single.html', context=context)


def contacts(request):
    popular_spaces, form, cities = get_side_objects()
    context = {'form': form,
               'cities': cities,
               'popular_spaces': popular_spaces,
               }
    return render(request, template_name='arenda_app/contacts.html', context=context)


def about(request):
    popular_spaces, form, cities = get_side_objects()
    context = {'form': form,
               'cities': cities,
               'popular_spaces': popular_spaces,
               }
    return render(request, template_name='arenda_app/about.html', context=context)