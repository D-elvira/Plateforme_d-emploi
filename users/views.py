from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

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
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # page d'accueil
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, 'users/connexion.html')


def choix_domaine_view(request):
    user_id = request.session.get('profiling_user_id')
    if request.method == 'POST':
        domaine = request.POST.get('domaine')
        # Ici tu peux sauvegarder le domaine dans ton modèle User ou Profil
        # Exemple: User.objects.filter(id=user_id).update(domaine=domaine)
        return redirect('home')  # après avoir choisi le domaine

    return render(request, 'choix_domaine.html')
