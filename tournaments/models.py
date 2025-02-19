from django.db import models
from PIL import Image
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    profile_picture = models.ImageField(upload_to="profile_pics", blank=True, default="pfp.png")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField("Nickname", max_length=17)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.nickname

    def save(self, *args, **kwargs):
        """
        Pradzioje leidziam padaryti issaugojimo veiksma,
        po to su fill biblioteka modifikuojam issaugoto pav. dydi
        """
        super().save(*args, **kwargs)  # numatytieji Model klases veiksmai suvykdomi
        if self.profile_picture.path:
            img = Image.open(self.profile_picture.path)
            thumb_size = (200, 200)
            img.thumbnail(thumb_size)
            img.save(self.profile_picture.path)


class Game(models.Model):
    name = models.CharField("name", max_length=100)
    description = models.TextField()
    release_date = models.DateField()

    def __str__(self):
        return self.name


class FavouriteGame(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('profile', 'game')

    def __str__(self):
        return f"{self.profile.nickname} - {self.game.name}"


class Tournament(models.Model):
    name = models.CharField("name", max_length=100)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    start_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TournamentParticipant(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('profile', 'tournament')

    def __str__(self):
        return f"{self.profile.nickname} - {self.tournament.name}"
