from django.shortcuts import render, redirect
from .models import City, Space, User
from django.contrib.auth.views import LoginView
from .forms import SelectSpaces, RegisterUserForm, LoginUserForm
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView
from django.urls import reverse_lazy


PAGE_LIMIT = 8


def clear_post(request):
    request.session['_old_post'] = None
    return redirect('index')


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
    if request.method == 'POST':
        request.session['_old_post'] = request.POST
        return redirect('index')
    side_context = get_side_context()
    spaces = Space.objects.all().order_by('-views')
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


def space_detail(request, space_id):
    if request.method == 'POST':
        request.session['_old_post'] = request.POST
        return redirect('index')
    side_context = get_side_context()
    if request.method == 'GET':
        space = get_object_or_404(Space, id=space_id)
        space.views += 1
        space.save()
    context = {'space': space,
               'images': space.images.all(),
               }
    context = {**context, **side_context}
    return render(request, template_name='arenda_app/single.html', context=context)


def contacts(request):
    if request.method == 'POST':
        request.session['_old_post'] = request.POST
        return redirect('index')
    context = get_side_context()
    return render(request, template_name='arenda_app/contacts.html', context=context)


def about(request):
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
        return super().post()

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
        return super().post()

    def get_success_url(self):
        url = reverse_lazy('index')
        return url

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context = {**context, **get_side_context()}
        return context
