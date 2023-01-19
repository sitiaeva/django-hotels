from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('1/', views.users_in_hotel_view, name='1'),
    path('2/', views.like_hotel_view, name='2'),
    path('3/', views.rooms_list_with_sold_out_sign_view, name='3'),
    path('4/', views.hotels_with_one_free_room_view, name='4'),
]
