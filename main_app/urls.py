from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name="logout"),
    path('', views.home, name='home'),
    path('playlist/', PlaylistListView.as_view(), name='playlist_list'),
    path('playlist/<int:pk>/add_song/', views.SongCreate.as_view(), name='add_song'),
    path('playlist/<mood>', views.playlist_detail, name='playlist_detail'),
    path('playlist/<int:playlist_id>/update/<int:pk>', views.SongUpdate.as_view(), name='songs_update'),
    path('playlist/<int:playlist_id>/delete/<int:pk>', views.SongDelete.as_view(), name='songs_delete'),
]
