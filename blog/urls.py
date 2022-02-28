from django.urls import path

from . import views

urlpatterns = [
    path('posts/all/', views.blog_post_gallery, name='allposts'),
    path('posts/new/', views.new_blog_post, name='newpost'),
    path('posts/<pk>', views.view_blog_post, name='viewpost')
]