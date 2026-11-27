from django.urls import path,include
from . import views

app_name = 'board'
urlpatterns = [
    path('blist/',views.blist,name='blist.html'),
    path('blist2/',views.blist2,name='blist2.html'),
]
