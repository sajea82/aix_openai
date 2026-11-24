from django.urls import path,include
from . import views

app_name='tour'
urlpatterns = [
    path('', views.tour,name='tour'),
]
