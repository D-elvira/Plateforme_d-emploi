from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from .models import User
from offres.models import Entreprise


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()

            if user.role == "recruteur":
                Entreprise.objects.create(
                    user=user,
                    nom=user.company_name or user.username,
                    ville=user.company_city or "",
                    domaine=user.company_domain or "",
                )
                login(request, user)
                messages.success(
                    request, "Bienvenue ! Votre espace recruteur est prêt."
                )
                return redirect("recruteur_dashboard")

            if user.role == "candidat":
                request.session["profiling_user_id"] = user.id
                messages.success(request, "Compte créé ! Choisissez vos domaines.")
                return redirect("choix_domaine")

            login(request, user)
            messages.success(request, "Votre compte a été créé avec succès !")
            return redirect("home")
        else:
            for field_name, error_list in form.errors.items():
                field_label = form.fields[field_name].label or field_name
                for error in error_list:
                    messages.error(request, f"{field_label} : {error}")
    else:
        form = UserRegisterForm()

    return render(request, "users/inscription.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        if not username or not password:
            messages.error(request, "Veuillez remplir tous les champs.")
            return render(request, "users/connexion.html")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Ravi de vous revoir, {username} !")
            next_url = request.GET.get("next") or request.POST.get("next", "")
            if next_url:
                return redirect(next_url)
            if user.is_staff:
                return redirect("admin_dashboard")
            if user.role == "recruteur":
                return redirect("recruteur_dashboard")
            return redirect("home")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, "users/connexion.html")


def choix_domaine_view(request):
    user_id = request.session.get("profiling_user_id")

    if not user_id:
        return redirect("register")

    if request.method == "POST":
        domaines_str = request.POST.get("domaines_selectionnes")

        try:
            user = User.objects.get(id=user_id)
            user.domaine_activite = domaines_str
            user.save()

            login(request, user)

            if "profiling_user_id" in request.session:
                del request.session["profiling_user_id"]

            messages.success(
                request,
                "Profil complété avec succès ! Voici les offres qui pourraient vous intéresser.",
            )
            return redirect("offres_list")

        except User.DoesNotExist:
            return redirect("register")

    return render(request, "users/choix_domaine.html")
