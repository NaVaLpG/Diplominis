from django.contrib import admin

from .models import Profile, Game, FavouriteGame, Tournament, TournamentParticipant, TournamentComment


admin.site.register(Profile)
admin.site.register(Game)
admin.site.register(FavouriteGame)
admin.site.register(Tournament)
admin.site.register(TournamentParticipant)
admin.site.register(TournamentComment)
