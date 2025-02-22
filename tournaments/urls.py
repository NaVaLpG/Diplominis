from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index_nm'),
    path('profile/', views.get_user_profile, name='user-profile'),
    path("register/", views.register_user, name="register"),
    path("games/", views.GameListView.as_view(), name="game-all"),
    path("games/<int:pk>", views.game_detail_view, name="game-one"),
    path("tournaments/", views.TournamentListView.as_view(), name="tournament-list"),
    path("tournaments/<int:pk>/", views.TournamentDetailView.as_view(), name="tournament-detail"),
    path('tournaments/<int:tournament_id>/upvote/', views.upvote_tournament, name='tournament-upvote'),
    path("tournaments/create/", views.TournamentCreateView.as_view(), name="tournament-create"),
    path('tournaments/<int:tournament_id>/join/', views.join_tournament, name='join-tournament'),
    path('tournaments/<int:tournament_id>/leave/', views.leave_tournament, name='leave-tournament'),
    path('game/<int:game_id>/add_favorite/', views.add_favorite_game, name='add-favorite-game'),
    path('game/<int:game_id>/remove_favorite/', views.remove_favorite_game, name='remove-favorite-game'),
    path("games/create/", views.GameCreateView.as_view(), name="game-create"),
    path('games/<int:pk>/update/', views.GameUpdateView.as_view(), name='game-update'),
]
