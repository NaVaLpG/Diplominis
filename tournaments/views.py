from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

from .forms import (ProfleUpdateForm,
                    TournamentStatusUpdateForm, TournamentForm,
                    TournamentRankingForm, GameForm,
                    GameUpdateForm, TournamentUpdateForm, TournamentCommentForm)
from .models import User, Profile, Game, Tournament, TournamentParticipant, FavouriteGame, TournamentComment


def index(request):
    """Main menu context return"""
    context = {"tournaments": Tournament.objects.all(),
               "upcoming_tournaments": Tournament.objects.filter(status="u").order_by("-id").all()[:5],
               "ongoing_tournaments": Tournament.objects.filter(status="o").order_by("-id").all()[:5],
               "completed_tournaments": Tournament.objects.filter(status="c").order_by("-id").all()[:5],
               "latest_games": Game.objects.order_by("-id").all()[:4],
               }

    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user=request.user)
        favorite_games = FavouriteGame.objects.filter(profile=profile).order_by("?").all()[:4]
        context["favourite_games"] = favorite_games
        print(favorite_games)

    return render(request, 'index.html', context=context)


@login_required()
@csrf_protect
def get_user_profile(request):
    """User profile context return"""
    profile = get_object_or_404(Profile, user=request.user)
    context = {
        "profile": profile,
        "tournaments": Tournament.objects.filter(tournamentparticipant__profile=profile).all()
    }
    return render(request, "profile.html", context=context)


@login_required()
@csrf_protect
def update_user_profile(request):
    """Allows user update his profile picture"""
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == "POST":
        p_form = ProfleUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
        return redirect("user-profile", )

    if request.method == "GET":
        p_form = ProfleUpdateForm(instance=request.user.profile)

        context = {
            "p_form": p_form,
            "profile": profile,
            "tournaments": Tournament.objects.filter(tournamentparticipant__profile=profile).all()
        }
    return render(request, "profile_update.html", context=context)


@csrf_protect
def register_user(request):
    """Registers new user and creates profile for it"""
    if request.method == "GET":
        return render(request, "registration/registration.html")
    elif request.method == "POST":
        # paimam duomenis is formos
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            messages.error(request, "Slaptazodziai nesutampa")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, f"Vartotojo vardas {username} uzsimtas")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Toks email jau yra uzimtas")
            return redirect("register")

        User.objects.create_user(username=username, email=email, password=password)
        messages.info(request, f"User {username} registered!")
        return redirect("login")


class GameListView(generic.ListView):
    """returns all games context and paginates it by 10"""
    model = Game
    context_object_name = "game_list"
    template_name = "games.html"
    paginate_by = 10


def game_detail_view(request, pk):
    """Allows user or guest inspect games"""
    game = get_object_or_404(Game, id=pk)
    is_favorite = False

    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user=request.user)
        is_favorite = FavouriteGame.objects.filter(profile=profile, game=game).exists()

    return render(request, "game.html", {"game": game, "is_favorite": is_favorite})


class TournamentListView(generic.ListView):
    """returns all tournaments and paginates tjem by 5"""
    model = Tournament
    template_name = "tournament_list.html"
    context_object_name = "tournaments"
    paginate_by = 5

    def get_queryset(self):
        return Tournament.objects.order_by("-id")


def get_upcoming_tournaments(request):
    """Gets all upcoming tournaments"""
    tournaments = Tournament.objects.filter(status="u")
    return render(request, "upcomming_tournaments.html", {"tournaments": tournaments})


def get_ongoing_tournaments(request):
    """Gets all ongoing tournaments"""
    tournaments = Tournament.objects.filter(status="o")
    return render(request, "ongoing_tournaments.html", {"tournaments": tournaments})


def get_completed_tournaments(request):
    """Gets all completed tournaments"""
    tournaments = Tournament.objects.filter(status="c")
    return render(request, "completed_tournaments.html", {"tournaments": tournaments})


class TournamentDetailView(generic.DetailView):
    """One tournaments detailed view"""
    model = Tournament
    template_name = "tournament_detail.html"

    def get_context_data(self, **kwargs):
        """Gets data about tournament ranking and comments"""
        context = super().get_context_data(**kwargs)
        tournament = self.object
        participants = tournament.tournamentparticipant_set.all().order_by('ranking')
        top_participants = tournament.tournamentparticipant_set.all().order_by('ranking')[:3]
        rest_participants = tournament.tournamentparticipant_set.all().order_by('ranking')[3:]

        if self.request.user.is_authenticated:
            user_participates = tournament.tournamentparticipant_set.filter(profile__user=self.request.user).exists()
            context['user_participates'] = user_participates

            if self.request.user == tournament.created_by or self.request.user.groups.filter(name="moderator").exists():
                context['status_form'] = TournamentStatusUpdateForm(instance=tournament)
            ranking_forms = {participant: TournamentRankingForm(instance=participant) for participant in participants}
            context['ranking_forms'] = ranking_forms
            context['can_rank'] = True

        context['comments'] = tournament.tournamentcomment_set.all().order_by('-date_created')
        context['comment_form'] = TournamentCommentForm()
        context['participants'] = participants
        context['top_participants'] = top_participants
        context['rest_participants'] = rest_participants

        return context

    def post(self, request, *args, **kwargs):
        tournament = self.get_object()

        if 'status_form' in request.POST:
            form = TournamentStatusUpdateForm(request.POST, instance=tournament)
            if form.is_valid():
                form.save()
            return redirect('tournament-detail', pk=tournament.pk)

        if 'ranking_form' in request.POST:
            if request.user == tournament.created_by or request.user.groups.filter(name="moderator").exists():
                participant_ids = request.POST.getlist("participant_id")

                for participant_id in participant_ids:
                    participant = get_object_or_404(TournamentParticipant, id=participant_id)

                    ranking_value = request.POST.get(f"ranking_{participant_id}")

                    if ranking_value:
                        participant.ranking = ranking_value
                        participant.save()
            return redirect('tournament-detail', pk=tournament.pk)

        if 'comment_form' in request.POST:
            comment_form = TournamentCommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.tournament = tournament
                comment.author = request.user
                comment.save()
            return redirect('tournament-detail', pk=tournament.pk)

        return redirect('tournament-detail', pk=tournament.pk)


@login_required
def join_tournament(request, tournament_id):
    """Allows player join tournament"""
    tournament = Tournament.objects.get(id=tournament_id)
    profile = Profile.objects.get(user=request.user)

    TournamentParticipant.objects.get_or_create(profile=profile, tournament=tournament)
    return redirect('tournament-detail', pk=tournament.id)


@login_required
def leave_tournament(request, tournament_id):
    """Allows player leave tournament"""
    tournament = Tournament.objects.get(id=tournament_id)
    profile = Profile.objects.get(user=request.user)

    TournamentParticipant.objects.filter(profile=profile, tournament=tournament).delete()
    return redirect('tournament-detail', pk=tournament.id)


# Sukurti naują turnyrą (tik prisijungusiems vartotojams)
class TournamentCreateView(LoginRequiredMixin, generic.CreateView):
    """Allows loggedin user create a new tournament"""
    model = Tournament
    form_class = TournamentForm
    template_name = "tournament_form.html"
    success_url = "/tournaments/tournaments/"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TournamentUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    """Allows user who created or site moderator update tournaments info"""
    model = Tournament
    form_class = TournamentUpdateForm
    template_name = "tournament_update.html"
    success_url = "/tournaments/tournaments/"

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        tournament = self.get_object()
        return self.request.user == tournament.created_by or self.request.user.groups.filter(name="moderator").exists()


class TournamentDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    """Allows moderators delete tournament"""
    model = Tournament
    template_name = "tournament_delete.html"
    success_url = "/tournaments/tournaments/"
    context_object_name = "tournament"

    def test_func(self):
        return self.request.user.groups.filter(name="moderator").exists()


class GameCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    """Allows moderators add a new game"""
    model = Game
    form_class = GameForm
    template_name = "game_form.html"
    success_url = "/tournaments/games/"

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.groups.filter(name="moderator").exists()


class GameUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    """Allows moderators update games info"""
    model = Game
    form_class = GameUpdateForm
    template_name = "game_update.html"
    success_url = "/tournaments/games/"

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.groups.filter(name="moderator").exists()


class GameDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    """Allows moderators delete game"""
    model = Game
    template_name = "game_delete.html"
    success_url = "/tournaments/games/"
    context_object_name = "game"

    def test_func(self):
        return self.request.user.groups.filter(name="moderator").exists()


@login_required
def add_favorite_game(request, game_id):
    """Allows a user to add a game to their favorites."""

    game = get_object_or_404(Game, id=game_id)
    profile, _ = Profile.objects.get_or_create(user=request.user)

    FavouriteGame.objects.get_or_create(profile=profile, game=game)

    return redirect('game-one', pk=game_id)


@login_required
def remove_favorite_game(request, game_id):
    """Allows a user to remove a game from their favorites"""
    game = get_object_or_404(Game, id=game_id)
    profile = get_object_or_404(Profile, user=request.user)

    FavouriteGame.objects.filter(profile=profile, game=game).delete()

    return redirect('game-one', pk=game_id)


@login_required
def upvote_tournament(request, tournament_id):
    """Allows user to upvote tournament"""
    tournament = get_object_or_404(Tournament, id=tournament_id)

    if request.user in tournament.upvotes.all():
        tournament.upvotes.remove(request.user)
    else:
        tournament.upvotes.add(request.user)

    return redirect('tournament-detail', pk=tournament.id)


def search_games(request):
    """Allows user to search for game"""
    query_text = request.GET.get('search_text')
    search_results = Game.objects.filter(name__icontains=query_text)

    context = {'query_text': query_text,
               'games': search_results}

    return render(request, 'game_search_results.html', context=context)


def search_tournaments(request):
    """Allows user to search turnament by game or name"""
    query_text = request.GET.get('search_text')
    search_results = Tournament.objects.filter(
        Q(name__icontains=query_text) |
        Q(game__name__icontains=query_text) |
        Q(created_by__username__icontains=query_text)
    )

    context = {'query_text': query_text,
               'tournaments': search_results}

    return render(request, 'tournament_search_results.html', context=context)


class TournamentCommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    """Allows moderators or creator to delete tournament"""
    model = TournamentComment
    template_name = "delete_comment.html"
    context_object_name = "comment"

    def get_success_url(self):
        comment_object = self.get_object()
        return reverse("tournament-detail", kwargs={"pk": comment_object.tournament.id})

    def test_func(self):
        moderator = False
        comment_object = self.get_object()
        ifself = self.request.user == comment_object.author
        for group in self.request.user.groups.all():
            if group == "moderator":
                moderator = True
        if moderator or ifself:
            return True
