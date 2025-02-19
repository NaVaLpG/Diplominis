from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index_nm'),
    path('profile/', views.get_user_profile, name='user-profile'),
    path("register/", views.register_user, name="register"),
    path("games/", views.GameListView.as_view(), name="game-all"),
    path("games/<int:pk>", views.GameDetailView.as_view(), name="game-one"),
    path("tournaments/", views.TournamentListView.as_view(), name="tournament-list"),
    path("tournaments/<int:pk>/", views.TournamentDetailView.as_view(), name="tournament-detail"),
    path("tournaments/create/", views.TournamentCreateView.as_view(), name="tournament-create"),

]
