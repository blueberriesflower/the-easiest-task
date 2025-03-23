from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('chat_rooms/', views.chat_rooms, name='chat_rooms'),
    path('create_chat_room/', views.create_chat_room, name='create_chat_room'),
    path('chat_room/<str:room_name>/', views.chat_room, name='chat_room'),
]