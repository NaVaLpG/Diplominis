from django import forms

from .models import Profile, User


class ProfleUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("profile_picture",)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)
