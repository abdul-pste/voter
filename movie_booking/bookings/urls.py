from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.movie_list, name='home'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    #path('book/<int:showtime_id>/', views.book_showtime, name='book_showtime'),
    path('booking/history/', views.booking_history, name='booking_history'),
    path('delete/history/', views.delete_all_bookings, name='delete_history'),
    path('profile/', views.profile, name='profile'),
    path('edit/profile/', views.edit_profile, name='edit_profile'),
    path('logout/', views.logout, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('book/<int:showtime_id>/', views.book_showtime, name='book_showtime'),
    path('movies/<int:movie_id>/add_showtime/', views.add_showtime, name='add_showtime'),
]
