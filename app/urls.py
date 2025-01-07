from django.urls import path
from . import views as app_views

urlpatterns = [
    path('', app_views.home, name='home'),
    path('search_results', app_views.search_results, name='search_results'),
    path('upload_song', app_views.upload_song, name='upload_song'),
    path('audio/<int:index>', app_views.serve_audio, name='serve_audio'),
    path('image/<int:index>', app_views.serve_image, name='serve_image'),
    path('new_upload', app_views.serve_new_uploaded_audio, name='serve_new_uploaded_audio'),
]
