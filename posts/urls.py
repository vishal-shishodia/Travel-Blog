from django.urls import path,include
from django.contrib.auth.views import LoginView
from .views import *

urlpatterns = [
    path('',index,name='index'),
    path('detail/<str:pk>/',DetailView,name='detail'),
    path('list/',ListView,name='list'),
    path('register/',Register,name='register'),
    path('login/',LoginView.as_view(template_name='login.html'),name='login'),
    path('create/',PostCreate,name='create'),
    path('update/<str:pk>/',PostUpdate,name='update'),
    path('delete/<str:pk>/',PostDelete,name='delete'),
    path('postComment/',postComment,name='postComment'),
    path('search/',search,name='search'),

]