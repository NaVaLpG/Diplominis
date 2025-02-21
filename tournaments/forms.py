from django import forms

from .models import Profile, User, Tournament


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
        fields = ['status']
