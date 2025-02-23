from django import forms

from .models import Profile, User, Tournament, TournamentParticipant, Game, TournamentComment


class ProfleUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("profile_picture",)


class TournamentStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ('status',)


class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ("name", "game", "start_date", "logo")


class TournamentUpdateForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ("name", "game", "start_date", "logo")


class TournamentRankingForm(forms.ModelForm):
    class Meta:
        model = TournamentParticipant
        fields = ('ranking',)


class TournamentCommentForm(forms.ModelForm):
    class Meta:
        model = TournamentComment
        fields = ("content", "tournament", "author")
        widgets = {
            "tournament": forms.HiddenInput(),
            "author": forms.HiddenInput()
        }


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ("name", "description", "release_date", "game_picture")


class GameUpdateForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ("name", "description", "release_date", "game_picture")


