from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from django.db.models import Q  # Q - kombinuoti keletą filtravimo sąlygų su OR
from django.core.paginator import Paginator  # funkcijų puslapiavimui
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

from .forms import UserUpdateForm, ProfleUpdateForm
from .models import User, Profile, Game, Tournament, TournamentParticipant


def index(request):
    return render(request, 'index.html')


@login_required()
@csrf_protect
def get_user_profile(request):
    if request.method == "POST":
        p_form = ProfleUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            messages.info(request, "Profilis atnaujintas")
        else:
            messages.error(request, "Profilis neatnaujinas. Ivyko klaida")
        return redirect("user-profile")

    if request.method == "GET":
        p_form = ProfleUpdateForm(instance=request.user.profile)
        u_form = UserUpdateForm(instance=request.user)

        context = {
            "p_form": p_form,
            "u_form": u_form
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


class GameDetailView(generic.DetailView):
    model = Game
    context_object_name = "game"
    template_name = "game.html"


class TournamentListView(generic.ListView):
    model = Tournament
    template_name = "tournament_list.html"
    context_object_name = "tournaments"


# Turnyro informacija
class TournamentDetailView(generic.DetailView):
    model = Tournament
    template_name = "tournament_detail.html"


# Sukurti naują turnyrą (tik prisijungusiems vartotojams)
class TournamentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Tournament
    template_name = "tournament_form.html"
    fields = ["name", "game", "start_date"]
    success_url = "/tournaments/tournaments/"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
