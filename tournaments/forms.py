from django import forms

from .models import Profile, User, Tournament, TournamentParticipant, Game


class ProfleUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("profile_picture",)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)


class TournamentStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ('status',)


class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ("name", "game", "start_date", "logo")


class TournamentRankingForm(forms.ModelForm):
    class Meta:
        model = TournamentParticipant
        fields = ('ranking',)


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ("name", "description", "release_date")


class GameUpdateForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ("name", "description", "release_date")
