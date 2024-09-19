from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Video upload page
    path('video_list/', views.video_list, name='video_list'),  # List of all uploaded videos
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),  # Detail view for a single video
    path('search/<int:video_id>/', views.search, name='search'),  # Search subtitles for a video

]