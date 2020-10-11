from django.urls import path,include
from .views import *

urlpatterns = [
    path('',index,name='index'),
    path('detail/<str:pk>/',DetailView,name='detail'),
    path('list/',ListView,name='list'),
    path('create/',PostCreate,name='create'),
    path('update/<str:pk>/',PostUpdate,name='update'),
    path('delete/<str:pk>/',PostDelete,name='delete'),

]