from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('clear_post', views.clear_post, name='clear_post'),
    path('<int:page>', views.index, name='index'),
    path('spaces/<int:space_id>', views.space_detail, name='space_detail'),
    path('about', views.about, name='about'),
    path('contacts', views.contacts, name='contacts'),
    path('register', views.RegisterUserView.as_view(), name='register'),
    path('login', views.LoginUser.as_view(), name='login'),
]