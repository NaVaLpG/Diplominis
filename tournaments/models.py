from django.db import models
from PIL import Image
from django.contrib.auth.models import User
from django.utils.timezone import now


# Create your models here.

class Profile(models.Model):
    """
    Stores user information.
    """
    profile_picture = models.ImageField(upload_to="profile_pics", default="pfp.png")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        """
        Overrides the save method to resize the profile picture before saving it.
        """
        super().save(*args, **kwargs)  # numatytieji Model klases veiksmai suvykdomi
        if self.profile_picture.path:
            img = Image.open(self.profile_picture.path)
            thumb_size = (200, 200)
            img.thumbnail(thumb_size)
            img.save(self.profile_picture.path)


class Game(models.Model):
    """
    Game model representing a video game entry with details such as name, description,
    release date, and an optional game picture.
    """
    game_picture = models.ImageField(upload_to="game_pics", default="game.png")
    name = models.CharField("name", max_length=100)
    description = models.TextField()
    release_date = models.DateField()

    def __str__(self):
        return self.name


class FavouriteGame(models.Model):
    """
    Model representing a many-to-many relationship between users (via Profile) and games.
    Ensures that each user can only mark a game as a favorite once.
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('profile', 'game')

    def __str__(self):
        return f"{self.profile} - {self.game.name}"


class Tournament(models.Model):
    """
    Model representing a tournament for a specific game.
    Tracks tournament details such as name, associated game, dates, creator, and status.
    """
    name = models.CharField("name", max_length=100)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    start_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    upvotes = models.ManyToManyField(User, related_name="tournament_upvotes", blank=True)
    logo = models.ImageField(upload_to='tournament_logos/', default="tournament.png")

    def total_upvotes(self):
        """Returns the total number of upvotes for the tournament."""
        return self.upvotes.count()

    STATUS_CHOICES = [
        ('u', 'Upcoming'),
        ('o', 'Ongoing'),
        ('c', 'Completed'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='u')
    end_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Overrides save method to automatically set end_date when the tournament is completed.
        """
        if self.status == 'c' and self.end_date is None:
            self.end_date = now().date()
        super().save(*args, **kwargs)

    @property
    def duration(self):
        """Calculates the duration of a completed tournament in days."""
        if self.status == 'c' and self.end_date:
            return (self.end_date - self.start_date).days
        return None

    def __str__(self):
        return self.name


class TournamentParticipant(models.Model):
    """
    Model representing participants in a tournament.
    Links users to tournaments and tracks their ranking.
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    ranking = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        """Ensures each participant is linked to a tournament only once"""
        unique_together = ('profile', 'tournament')

    def __str__(self):
        return f"{self.profile} - {self.tournament.name}"


class TournamentComment(models.Model):
    """
    Model for user comments on tournaments.
    Stores content, timestamp, and links to the author and tournament.
    """
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField("Comment", max_length=2000)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.date_created} {self.author},{self.tournament}, {self.content[:50]}"
