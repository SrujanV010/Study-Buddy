from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    
    path('', views.home, name = 'home'),#set the path home which is default whe=ich occurs when website is opened
    path('room/<str:pk>/', views.room, name = 'room'),#go to url http://127.0.0.1:8000/room/ to get into any room
    path('create-room/', views.createRoom, name = "create-room" ),
    path('update-room/<str:pk>/', views.updateRoom, name = 'update-room'),
    path('delete-room/<str:pk>/', views.deleteRoom, name = 'delete-room'),

    path('delete-msg/<str:pk>/', views.deleteMsg, name='deleteMsg'),

    path('profile/<str:pk>/',views.userProfile, name = 'profile'),
    path('update-user/', views.updateUser, name = 'update-user'),
    path('topics/', views.topicsPage, name='topics'),
    path('activity/', views.activityPage, name='activity'),
]



