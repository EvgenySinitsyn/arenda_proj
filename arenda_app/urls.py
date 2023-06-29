from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('clear_post', views.clear_post, name='clear_post'),
    path('<int:page>', views.index, name='index'),
    path('spaces/<int:space_id>', views.space_detail, name='space_detail'),
]