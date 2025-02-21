from lib2to3.fixes.fix_input import context

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

from .forms import UserUpdateForm, ProfleUpdateForm, TournamentStatusUpdateForm
from .models import User, Profile, Game, Tournament, TournamentParticipant, FavouriteGame


def index(request):
    return render(request, 'index.html')


@login_required()
@csrf_protect
def get_user_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == "POST":
        p_form = ProfleUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            messages.info(request, "Profilis atnaujintas")
        else:
            messages.error(request, "Profilis neatnaujinas. Ivyko klaida")
        return redirect("user-profile", )

    if request.method == "GET":
        p_form = ProfleUpdateForm(instance=request.user.profile)
        u_form = UserUpdateForm(instance=request.user)

        context = {
            "p_form": p_form,
            "u_form": u_form,
            "profile": profile,
        }
    return render(request, "profile.html", context=context)


@csrf_protect
def register_user(request):
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
        messages.info(request, f"Vartotojas {username} sekmingai uzregistruotas!")
        return redirect("login")


class GameListView(generic.ListView):
    model = Game
    context_object_name = "game_list"
    template_name = "games.html"
    paginate_by = 3


def game_detail_view(request, pk):
    game = get_object_or_404(Game, id=pk)
    is_favorite = False

    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user=request.user)
        is_favorite = FavouriteGame.objects.filter(profile=profile, game=game).exists()

    return render(request, "game.html", {"game": game, "is_favorite": is_favorite})


class TournamentListView(generic.ListView):
    model = Tournament
    template_name = "tournament_list.html"
    context_object_name = "tournaments"


# Turnyro informacija
class TournamentDetailView(generic.DetailView):
    model = Tournament
    template_name = "tournament_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tournament = self.object  # Gauname turnyro objektą

        # Patikriname, ar vartotojas dalyvauja turnyre
        if self.request.user.is_authenticated:
            user_participates = tournament.tournamentparticipant_set.filter(profile__user=self.request.user).exists()
            context['user_participates'] = user_participates

            if self.request.user == tournament.created_by or self.request.user.groups.filter(name="moderator").exists():
                context['status_form'] = TournamentStatusUpdateForm(instance=tournament)

        return context

    def post(self, request, *args, **kwargs):
        """Handle the status update"""
        tournament = self.get_object()

        form = TournamentStatusUpdateForm(request.POST, instance=tournament)
        if form.is_valid():
            form.save()
        return redirect('tournament-detail', pk=tournament.pk)


@login_required
def join_tournament(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    profile = Profile.objects.get(user=request.user)

    TournamentParticipant.objects.get_or_create(profile=profile, tournament=tournament)
    return redirect('tournament-detail', pk=tournament.id)


@login_required
def leave_tournament(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    profile = Profile.objects.get(user=request.user)

    TournamentParticipant.objects.filter(profile=profile, tournament=tournament).delete()
    return redirect('tournament-detail', pk=tournament.id)


# Sukurti naują turnyrą (tik prisijungusiems vartotojams)
class TournamentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Tournament
    template_name = "tournament_form.html"
    fields = ["name", "game", "start_date"]
    success_url = "/tournaments/tournaments/"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


@login_required
def add_favorite_game(request, game_id):
    """Allows a user to add a game to their favorites"""
    game = get_object_or_404(Game, id=game_id)
    profile = get_object_or_404(Profile, user=request.user)

    # Check if the game is already in favorites
    favorite, created = FavouriteGame.objects.get_or_create(profile=profile, game=game)

    if created:
        messages.success(request, f"{game.name} added to favorites!")
    else:
        messages.info(request, f"{game.name} is already in your favorites.")

    return redirect('game-one', pk=game_id)


@login_required
def remove_favorite_game(request, game_id):
    """Allows a user to remove a game from their favorites"""
    game = get_object_or_404(Game, id=game_id)
    profile = get_object_or_404(Profile, user=request.user)

    # Delete the favorite if it exists
    FavouriteGame.objects.filter(profile=profile, game=game).delete()
    messages.success(request, f"{game.name} removed from favorites!")

    return redirect('game-one', pk=game_id)


@login_required
def upvote_tournament(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)

    if request.user in tournament.upvotes.all():
        tournament.upvotes.remove(request.user)
    else:
        tournament.upvotes.add(request.user)

    return redirect('tournament-detail', pk=tournament.id)
