from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from .models import User

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)  # ne pas sauvegarder tout de suite
            # Hachage du mot de passe
            user.set_password(form.cleaned_data['password1'])
            user.save()  # maintenant l'utilisateur est créé correctement

            messages.success(request, "Votre compte a été créé avec succès !")

            # Si c'est un candidat, on stocke son id pour le choix du domaine
            if user.role == 'candidat':
                request.session['profiling_user_id'] = user.id
                return redirect('choix_domaine')  # page du choix de domaine
            else:
                return redirect('login')  # pour un recruteur, retour à la connexion
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = UserRegisterForm()

    return render(request, 'users/inscription.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        # On utilise .get() pour éviter l'erreur MultiValueDictKeyError si le champ est vide
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # Vérification de sécurité de base
        if not username or not password:
            messages.error(request, "Veuillez remplir tous les champs.")
            return render(request, 'users/connexion.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Ravi de vous revoir, {username} !")
            return redirect('home')
        else:
            # Si on arrive ici, c'est soit le mauvais MDP, soit l'utilisateur n'existe pas
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'users/connexion.html')


def choix_domaine_view(request):
    user_id = request.session.get('profiling_user_id')

    # Sécurité : si on arrive ici sans id en session, on renvoie à l'inscription
    if not user_id:
        return redirect('register')

    if request.method == 'POST':
        # On récupère la chaîne de caractères (ex: "Informatique,BTP,Santé")
        domaines_str = request.POST.get('domaines_selectionnes')

        try:
            user = User.objects.get(id=user_id)
            # On enregistre la chaîne dans le champ domaine_activite
            user.domaine_activite = domaines_str
            user.save()

            # Connexion automatique de l'utilisateur
            login(request, user)

            # Nettoyer la session après usage pour éviter les conflits
            if 'profiling_user_id' in request.session:
                del request.session['profiling_user_id']

            messages.success(request, "Profil complété avec succès ! Voici les offres qui pourraient vous intéresser.")

            # Redirection directe vers la liste des offres (ou home si tu as mis les offres sur la home)
            return redirect('offres_list')

        except User.DoesNotExist:
            return redirect('register')

    return render(request, 'users/choix_domaine.html')