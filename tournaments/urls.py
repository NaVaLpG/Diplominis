from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index_nm'),
    path('profile/', views.get_user_profile, name='user-profile'),
    path('profile/update/', views.update_user_profile, name='user-profile-update'),
    path("register/", views.register_user, name="register"),
    path("games/", views.GameListView.as_view(), name="game-all"),
    path("games/<int:pk>", views.game_detail_view, name="game-one"),
    path("tournaments/", views.TournamentListView.as_view(), name="tournament-list"),
    path("tournaments/<int:pk>/", views.TournamentDetailView.as_view(), name="tournament-detail"),
    path('tournaments/<int:tournament_id>/upvote/', views.upvote_tournament, name='tournament-upvote'),
    path("tournaments/create/", views.TournamentCreateView.as_view(), name="tournament-create"),
    path('tournaments/<int:tournament_id>/join/', views.join_tournament, name='join-tournament'),
    path('tournaments/<int:tournament_id>/leave/', views.leave_tournament, name='leave-tournament'),
    path('games/<int:game_id>/add_favorite/', views.add_favorite_game, name='add-favorite-game'),
    path('games/<int:game_id>/remove_favorite/', views.remove_favorite_game, name='remove-favorite-game'),
    path("games/create/", views.GameCreateView.as_view(), name="game-create"),
    path('games/<int:pk>/update/', views.GameUpdateView.as_view(), name='game-update'),
    path('games/<int:pk>/delete/', views.GameDeleteView.as_view(), name='game-delete'),
    path("games/search/", views.search_games, name="game_search"),
    path("tournaments/search/", views.search_tournaments, name="tournament_search"),
    path("tournaments/<int:pk>/update/", views.TournamentUpdateView.as_view(), name="tournament-update"),
    path("tournaments/<int:pk>/delete/", views.TournamentDeleteView.as_view(), name="tournament-delete"),
    path("tournaments/upcomming/", views.get_upcoming_tournaments, name="upcomming-tournaments"),
    path("tournaments/ongoing/", views.get_ongoing_tournaments, name="ongoing-tournaments"),
    path("tournaments/completed/", views.get_completed_tournaments, name="completed-tournaments"),
    path("books/comment/<int:pk>", views.TournamentCommentDeleteView.as_view(), name="comment-delete"),

]
