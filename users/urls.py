from django.urls import path
from . import views  # Attention aux imports circulaires
from users import views as users_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('deconnexion/', LogoutView.as_view(next_page='home'), name='logout'),
    path('choix_domaine/', users_views.choix_domaine_view, name='choix_domaine'),  # <-- corrigé

]
