from django import forms

from .models import Profile, Tournament, TournamentParticipant, Game, TournamentComment


class ProfleUpdateForm(forms.ModelForm):
    """
    Form for updating a user's profile picture.
    """
    class Meta:
        model = Profile
        fields = ("profile_picture",)


class TournamentStatusUpdateForm(forms.ModelForm):
    """
    Form for updating the status of a tournament.
    """
    class Meta:
        model = Tournament
        fields = ('status',)


class TournamentForm(forms.ModelForm):
    """
     Form for creating a new tournament with required details.
     """
    class Meta:
        model = Tournament
        fields = ("name", "game", "start_date", "logo")


class TournamentUpdateForm(forms.ModelForm):
    """
    Form for updating an existing tournament's details.
    """
    class Meta:
        model = Tournament
        fields = ("name", "game", "start_date", "logo")


class TournamentRankingForm(forms.ModelForm):
    """
    Form for updating the ranking of a tournament participant.
    """
    class Meta:
        model = TournamentParticipant
        fields = ('ranking',)


class TournamentCommentForm(forms.ModelForm):
    """
    Form for adding a comment to a tournament.
    The tournament and author fields are hidden and set automatically.
    """
    class Meta:
        model = TournamentComment
        fields = ("content", "tournament", "author")
        widgets = {
            "tournament": forms.HiddenInput(),
            "author": forms.HiddenInput()
        }


class GameForm(forms.ModelForm):
    """
    Form for creating a new game with relevant details.
    """
    class Meta:
        model = Game
        fields = ("name", "description", "release_date", "game_picture")


class GameUpdateForm(forms.ModelForm):
    """
    Form for updating an existing game's details.
    """
    class Meta:
        model = Game
        fields = ("name", "description", "release_date", "game_picture")


class GameTournamentForm(forms.ModelForm):
    """
    Form for creating a tournament associated with a specific game.
    The game field is hidden and set automatically.
    """
    class Meta:
        model = Tournament
        fields = ("name", "start_date", "logo")
        widgets = {"game": forms.HiddenInput()}
