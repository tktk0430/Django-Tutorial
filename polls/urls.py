from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('aaa', views.aaa, name='aaa')
]