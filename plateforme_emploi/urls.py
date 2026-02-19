# On importe le module admin pour l'interface d'administration de Django
from django.contrib import admin
# On importe path et include pour définir les routes (URLs)
from django.urls import path, include
# On importe settings pour accéder aux paramètres du projet
from django.conf import settings
# On importe static pour servir les fichiers médias (images, PDF, etc.) en développement
from django.conf.urls.static import static
from offres.views import home
from users import views as users_views



# Liste des URLs principales du projet

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('offres/', include('offres.urls')),
    path('candidatures/', include('candidatures.urls')),
path('choix_domaine/', users_views.choix_domaine_view, name='choix_domaine'),]
# Configuration pour servir les fichiers médias (images uploadées) pendant le développement
# settings.MEDIA_URL → chemin public pour accéder aux fichiers médias (ex: '/media/')
# settings.MEDIA_ROOT → chemin réel sur le serveur où les fichiers sont stockés
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
