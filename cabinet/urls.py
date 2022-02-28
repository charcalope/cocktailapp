from django.urls import path

from . import views

urlpatterns = [
    path('cabinet/', views.view_cabinet, name='cabinet'),
    path('cabinet/search/', views.search_for_cabinet, name='cabinetsearch'),
    path('cabinet/<pk>/add', views.add_to_cabinet, name='addtocabinet'),
    path('cabinet/<pk>/delete', views.delete_from_cabinet, name='deletefromcabinet'),
]