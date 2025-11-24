from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('sqlipwn/scripts/api/add_comment', views.add_comment, name='add_comment'),
  path('sqlipwn/scripts/api/list_comments', views.list_comments, name='list_comments')
]
