from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name="logout"),
    path('', HomeView.as_view(), name='home'),
    path('playlist/', PlaylistListView.as_view(), name='playlist_list'),
    path('playlist/<int:pk>/', PlaylistDetailView.as_view(), name='playlist_detail'),
    path('playlist/create/', PlaylistCreate.as_view(), name='playlist_create'),
]