from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import City, Space, User, Building, RentType, SpaceType, SpaceImage
from django.contrib.auth.views import LoginView
from .forms import SelectSpaces, RegisterUserForm, LoginUserForm, BuildingForm, SpaceForm
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


PAGE_LIMIT = 8


def clear_post(request):
    request.session['_old_post'] = None
    return redirect('index')


def clear_space_add(request):
    request.session['_add_building'] = None
    request.session['_add_space'] = None


def get_side_context():
    popular_spaces = Space.objects.all().order_by('-views')[:2]
    form = SelectSpaces()
    cities = City.objects.all()
    side_context = {'filter_form': form,
                    'cities': cities,
                    'popular_spaces': popular_spaces,
                    }
    return side_context


def filter_spaces(spaces, post):
    if post['type']:
        spaces = spaces.filter(type_id=post['type'])
    if post['rent_type']:
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
    clear_space_add(request)
    if request.method == 'POST':
        request.session['_old_post'] = request.POST
        return redirect('index')
    side_context = get_side_context()
    spaces = Space.objects.all().order_by('-created_tm', '-views')
    old_post = request.session.get('_old_post')
    if old_post:
        spaces = filter_spaces(spaces, old_post)
        side_context['filter_form'] = SelectSpaces(old_post)
    page_spaces = spaces[(page - 1) * PAGE_LIMIT:((page - 1) * PAGE_LIMIT) + PAGE_LIMIT]
    page_count = len(spaces) // PAGE_LIMIT + 1
    context = {'spaces': page_spaces,
               'page_count': range(1, page_count + 1),
               'pages_amount': page_count,
               'current_page': page,
               }
    context = {**context, **side_context}
    return render(request, template_name='arenda_app/index.html', context=context)


@login_required(login_url='login')
def space_detail(request, space_id):
    clear_space_add(request)
    if request.method == 'POST':
        request.session['_old_post'] = request.POST
        return redirect('index')
    side_context = get_side_context()
    if request.method == 'GET':
        space = get_object_or_404(Space, id=space_id)
        space.views += 1
        space.save()
    print(space.owner.phone)
    context = {'space': space,
               'images': space.images.all(),
               }
    context = {**context, **side_context}
    return render(request, template_name='arenda_app/single.html', context=context)


def contacts(request):
    clear_space_add(request)
    if request.method == 'POST':
        request.session['_old_post'] = request.POST
        return redirect('index')
    context = get_side_context()
    return render(request, template_name='arenda_app/contacts.html', context=context)


def about(request):
    clear_space_add(request)
    if request.method == 'POST':
        request.session['_old_post'] = request.POST
        return redirect('index')
    context = get_side_context()
    return render(request, template_name='arenda_app/about.html', context=context)


class RegisterUserView(CreateView):
    model = User
    form_class = RegisterUserForm
    template_name = 'arenda_app/register.html'
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        if 'filter_form' in request.POST:
            request.session['_old_post'] = request.POST
            return redirect('index')
        return super().post(request)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context = {**context, **get_side_context()}
        return context


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'arenda_app/login.html'

    def post(self, request, *args, **kwargs):
        if 'filter_form' in request.POST:
            request.session['_old_post'] = request.POST
            return redirect('index')
        return super().post(request)

    def get_success_url(self):
        url = reverse_lazy('index')
        return url

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context = {**context, **get_side_context()}
        return context


def logout_user(request):
    logout(request)
    return redirect('index')


@login_required(login_url='login')
def add_space(request):
    context = get_side_context()
    if request.method == 'GET':
        _add_building = request.session.get('_add_building')
        if not _add_building:
            context['stage'] = 'building'
            context['text'] = 'Введите адрес'
            context['cities'] = City.objects.all()
            context['streets'] = Building.objects.values('street').distinct()
            context['numbers'] = Building.objects.values('number').distinct()
            context['building_form'] = BuildingForm
            return render(request, 'arenda_app/add_space.html', context)
        _add_space = request.session.get('_add_space')
        if not _add_space:
            context['stage'] = 'space'
            context['text'] = 'Опишите помещение'
            context['space_form'] = SpaceForm
            return render(request, 'arenda_app/add_space.html', context)
        else:
            return redirect('index')
    else:
        if 'building_form' in request.POST:
            request.session['_add_building'] = request.POST
            return redirect('add_space')
        if 'space_form' in request.POST:
            building_data = request.session.get('_add_building')
            city = City.objects.get_or_create(name=building_data['city'])[0]
            building = {
                'city': city,
                'street': building_data['street'],
                'number': building_data['number'],
            }
            building = Building.objects.get_or_create(**building)
            space_data = SpaceForm(request.POST)
            print(space_data.data)

            space = {
                'building': building[0],
                'day_price': space_data.data['day_price'],
                'month_price': space_data.data['month_price'],
                'type': SpaceType.objects.get(id=space_data.data['type']),
                'rent_type': RentType.objects.get(id=space_data.data['rent_type']),
                'area': space_data.data['area'],
                'rooms_number': space_data.data['rooms_number'],
                'description': space_data.data['description'],
                'owner': request.user,
            }
            space = Space.objects.create(**space)
            images = request.FILES.getlist('images')
            for image in images:
                SpaceImage.objects.create(space=space, image=image)
            return redirect(f'spaces/{space.id}')
        else:
            request.session['_old_post'] = request.POST
            return redirect('index')

