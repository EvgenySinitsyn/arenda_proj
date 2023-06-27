from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('spaces', views.show_spaces, name='spaces'),
]