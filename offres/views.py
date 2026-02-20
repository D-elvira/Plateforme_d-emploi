from django.shortcuts import render, get_object_or_404, redirect
from .models import Offre, Candidature
from .forms import CandidatureForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
import re


def home(request):
    offres = Offre.objects.filter(statut="disponible").order_by("-id")

    if (
        request.user.is_authenticated
        and hasattr(request.user, "domaine_activite")
        and request.user.domaine_activite
    ):
        domaines_utilisateur = request.user.domaine_activite.split(",")
        offres_personnalisees = offres.filter(categorie__in=domaines_utilisateur)[:6]
        if offres_personnalisees.exists():
            return render(
                request,
                "home.html",
                {"offres": offres_personnalisees, "personnalise": True},
            )

    return render(request, "home.html", {"offres": offres[:6], "personnalise": False})


# Synonymes et termes associés pour enrichir la recherche
SYNONYMES = {
    # Informatique
    "informatique": [
        "développeur",
        "programmeur",
        "codeur",
        "logiciel",
        "software",
        "web",
        "data",
        "réseau",
        "système",
        "it",
        "tech",
        "numérique",
        "digital",
        "ordinateur",
    ],
    "développeur": [
        "dev",
        "programmeur",
        "codeur",
        "fullstack",
        "frontend",
        "backend",
        "développement",
    ],
    "web": [
        "site",
        "internet",
        "frontend",
        "backend",
        "fullstack",
        "html",
        "css",
        "javascript",
        "react",
        "django",
        "php",
    ],
    "cybersécurité": [
        "sécurité",
        "security",
        "pare-feu",
        "firewall",
        "pentest",
        "hacking",
        "réseau",
        "cyber",
    ],
    "data": [
        "données",
        "analyse",
        "statistique",
        "science",
        "machine learning",
        "ia",
        "intelligence artificielle",
        "big data",
        "base de données",
    ],
    "réseau": [
        "network",
        "cisco",
        "télécom",
        "infrastructure",
        "admin système",
        "système",
    ],
    # Gestion / Finance
    "comptabilité": [
        "comptable",
        "finance",
        "financier",
        "audit",
        "fiscal",
        "trésorerie",
        "bilan",
        "gestion",
    ],
    "finance": [
        "banque",
        "financier",
        "comptabilité",
        "investissement",
        "trésorerie",
        "économie",
        "bourse",
    ],
    "gestion": [
        "management",
        "administration",
        "organisation",
        "pilotage",
        "coordonnateur",
        "gestionnaire",
        "administratif",
    ],
    "rh": [
        "ressources humaines",
        "recrutement",
        "paie",
        "formation",
        "personnel",
        "talent",
    ],
    # Marketing / Communication
    "marketing": [
        "publicité",
        "promotion",
        "marque",
        "brand",
        "stratégie",
        "communication",
        "digital",
        "seo",
        "référencement",
        "community manager",
    ],
    "communication": [
        "média",
        "presse",
        "journalisme",
        "rédaction",
        "contenu",
        "community",
    ],
    "design": [
        "graphique",
        "graphiste",
        "ui",
        "ux",
        "visuel",
        "créatif",
        "photoshop",
        "illustrator",
        "maquette",
    ],
    # Ingénierie
    "ingénieur": [
        "ingénierie",
        "technique",
        "génie",
        "civil",
        "mécanique",
        "électrique",
        "industriel",
    ],
    "mécanique": ["machine", "moteur", "automobile", "maintenance", "production"],
    "électrique": [
        "électronique",
        "énergie",
        "électricité",
        "automatisme",
        "électrotechnique",
    ],
    "civil": [
        "bâtiment",
        "construction",
        "architecture",
        "btp",
        "chantier",
        "génie civil",
    ],
    # Santé
    "santé": [
        "médecin",
        "infirmier",
        "pharmacie",
        "hôpital",
        "médical",
        "clinique",
        "soins",
    ],
    # Droit
    "droit": ["juridique", "avocat", "notaire", "juriste", "légal", "contrat"],
    # Éducation
    "éducation": [
        "enseignement",
        "professeur",
        "formateur",
        "pédagogie",
        "école",
        "formation",
    ],
    # Agriculture
    "agriculture": [
        "agronome",
        "agronomie",
        "ferme",
        "culture",
        "élevage",
        "environnement",
    ],
}

# Stop words français étendus
STOP_WORDS = {
    "je",
    "suis",
    "un",
    "une",
    "de",
    "du",
    "des",
    "le",
    "la",
    "les",
    "en",
    "et",
    "ou",
    "pour",
    "mon",
    "ma",
    "mes",
    "qui",
    "que",
    "dans",
    "avec",
    "sur",
    "par",
    "ce",
    "cette",
    "ces",
    "au",
    "aux",
    "il",
    "elle",
    "nous",
    "vous",
    "ils",
    "elles",
    "à",
    "a",
    "ai",
    "as",
    "est",
    "son",
    "sa",
    "ses",
    "ne",
    "pas",
    "plus",
    "aussi",
    "très",
    "trop",
    "bien",
    "bon",
    "faire",
    "fait",
    "été",
    "être",
    "avoir",
    "veux",
    "voudrais",
    "souhaite",
    "aimerai",
    "aimerais",
    "besoin",
    "endroit",
    "lieu",
    "trouver",
    "où",
    "comment",
    "quoi",
    "quel",
    "quelle",
    "bref",
    "donc",
    "car",
    "mais",
    "depuis",
    "tout",
    "tous",
    "toute",
    "toutes",
    "ça",
    "cela",
    "ceci",
    "là",
    "ici",
    "si",
    "quand",
    "comme",
    "même",
    "encore",
    "déjà",
    "après",
    "avant",
    "entre",
    "vers",
    "chez",
    "sous",
    "sans",
    "contre",
    "parce",
    "its",
    "dont",
    "voici",
    "voilà",
    "peut",
    "peux",
    "puis",
    "serait",
    "sera",
    "ont",
    "sont",
    "était",
    "avait",
    "pourrait",
    "devrait",
}


def extraire_mots_cles(query):
    """Extrait les mots significatifs d'une phrase en langage naturel."""
    query_lower = query.lower().strip()
    # Normaliser les accents courants
    words = re.findall(r"[a-zàâäéèêëïîôùûüç\-]+", query_lower)
    keywords = [w for w in words if w not in STOP_WORDS and len(w) > 2]
    return keywords


def enrichir_mots_cles(keywords):
    """Enrichit les mots-clés avec des synonymes et termes associés."""
    enriched = set(keywords)
    for kw in keywords:
        # Chercher directement dans les synonymes
        if kw in SYNONYMES:
            enriched.update(SYNONYMES[kw])
        # Chercher aussi dans les valeurs (associations inversées)
        for key, synonyms in SYNONYMES.items():
            if kw in synonyms or any(kw in s for s in synonyms):
                enriched.add(key)
                enriched.update(synonyms)
    return list(enriched)


def detecter_type_categorie(query_lower):
    """Détecte le type d'offre et la catégorie demandés."""
    type_filter = None
    categorie_filter = None

    # Détection du type
    stage_words = ["stage", "stagiaire", "stages"]
    emploi_words = [
        "emploi",
        "travail",
        "poste",
        "job",
        "cdi",
        "cdd",
        "contrat",
        "embauche",
        "recrute",
    ]

    if any(w in query_lower for w in stage_words):
        type_filter = "stage"
    elif any(w in query_lower for w in emploi_words):
        type_filter = "emploi"

    # Détection de la catégorie
    if any(
        w in query_lower
        for w in [
            "académique",
            "academique",
            "universitaire",
            "université",
            "ecole",
            "école",
            "étude",
            "etude",
            "scolaire",
            "licence",
            "master",
            "bts",
            "dut",
        ]
    ):
        categorie_filter = "academique"
    elif any(
        w in query_lower
        for w in ["professionnel", "professionnelle", "pro", "entreprise"]
    ):
        categorie_filter = "professionnel"

    return type_filter, categorie_filter


def detecter_ville(query_lower, keywords):
    """Détecte les villes mentionnées dans la requête."""
    villes_cameroun = [
        "douala",
        "yaoundé",
        "yaounde",
        "bafoussam",
        "bamenda",
        "garoua",
        "maroua",
        "ngaoundéré",
        "ngaoundere",
        "bertoua",
        "ebolowa",
        "kribi",
        "limbe",
        "buea",
        "kumba",
        "edéa",
        "nkongsamba",
        "dschang",
        "foumban",
        "loum",
        "sangmélima",
    ]
    for ville in villes_cameroun:
        if ville in query_lower:
            return ville
    return None


def scorer_offre(
    offre, keywords, enriched_keywords, type_filter, categorie_filter, ville
):
    """Calcule un score de pertinence pour une offre. Plus le score est haut, plus l'offre est pertinente."""
    score = 0
    texte_offre = f"{offre.titre} {offre.profil_recherche} {offre.attentes} {offre.ville} {offre.entreprise.nom} {offre.entreprise.domaine or ''}".lower()

    # 1. Correspondance exacte des mots-clés originaux (poids fort)
    for kw in keywords:
        if kw in texte_offre:
            # Plus le mot apparaît, plus le score monte
            count = texte_offre.count(kw)
            score += 15 * min(count, 3)  # Max 45 pts par mot-clé original
            # Bonus si dans le titre
            if kw in offre.titre.lower():
                score += 20

    # 2. Correspondance des synonymes enrichis (poids moyen)
    for kw in enriched_keywords:
        if kw not in keywords and kw in texte_offre:
            count = texte_offre.count(kw)
            score += 8 * min(count, 2)  # Max 16 pts par synonyme
            if kw in offre.titre.lower():
                score += 10

    # 3. Correspondance type exacte (bonus fort)
    if type_filter and offre.type == type_filter:
        score += 30

    # 4. Correspondance catégorie exacte (bonus fort)
    if categorie_filter and offre.categorie == categorie_filter:
        score += 25

    # 5. Correspondance ville
    if ville:
        if ville in offre.ville.lower():
            score += 35
        elif ville in (offre.entreprise.ville or "").lower():
            score += 25

    # 6. Bonus si l'offre est disponible (déjà filtré mais quand même)
    if offre.statut == "disponible":
        score += 5

    return score


def recherche_intelligente(request):
    """API de recherche intelligente en langage naturel."""
    query = request.GET.get("q", "").strip()
    if not query:
        return JsonResponse(
            {"offres": [], "message": "Décrivez ce que vous recherchez."}
        )

    query_lower = query.lower()

    # 1. Extraction des mots-clés
    keywords = extraire_mots_cles(query)

    # 2. Enrichissement avec synonymes
    enriched = enrichir_mots_cles(keywords)

    # 3. Détection du type et catégorie
    type_filter, categorie_filter = detecter_type_categorie(query_lower)

    # 4. Détection de la ville
    ville = detecter_ville(query_lower, keywords)

    # 5. Filtre initial large — on prend toutes les offres disponibles
    offres = Offre.objects.filter(statut="disponible").select_related("entreprise")

    # 6. Pré-filtre par type si détecté (accélère la recherche)
    if type_filter:
        offres_filtrees = offres.filter(type=type_filter)
        # Si pas assez de résultats, on élargit
        if offres_filtrees.count() < 2:
            offres_filtrees = offres
    else:
        offres_filtrees = offres

    # 7. Recherche textuelle large : on combine mots-clés ET synonymes
    all_search_terms = set(keywords + enriched)
    if all_search_terms:
        q_objects = Q()
        for term in all_search_terms:
            if len(term) > 2:
                q_objects |= (
                    Q(titre__icontains=term)
                    | Q(profil_recherche__icontains=term)
                    | Q(attentes__icontains=term)
                    | Q(ville__icontains=term)
                    | Q(entreprise__nom__icontains=term)
                    | Q(entreprise__domaine__icontains=term)
                )
        offres_candidates = offres_filtrees.filter(q_objects).distinct()
    else:
        offres_candidates = offres_filtrees

    # 8. Si aucun résultat avec les filtres, chercher dans toutes les offres
    if not offres_candidates.exists() and all_search_terms:
        q_objects = Q()
        for term in all_search_terms:
            if len(term) > 2:
                q_objects |= (
                    Q(titre__icontains=term)
                    | Q(profil_recherche__icontains=term)
                    | Q(attentes__icontains=term)
                )
        offres_candidates = offres.filter(q_objects).distinct()

    # 9. Scorer et classer chaque offre
    scored_offres = []
    for offre in offres_candidates[:50]:  # Limiter à 50 pour la performance
        score = scorer_offre(
            offre, keywords, enriched, type_filter, categorie_filter, ville
        )
        if score > 0:
            scored_offres.append((offre, score))

    # Trier par score décroissant
    scored_offres.sort(key=lambda x: x[1], reverse=True)

    # 10. Normaliser les scores (0-100%)
    max_score = scored_offres[0][1] if scored_offres else 1
    top_offres = scored_offres[:12]

    offres_data = []
    for offre, score in top_offres:
        score_normalized = round((score / max_score) * 100)
        offres_data.append(
            {
                "id": offre.id,
                "titre": offre.titre,
                "entreprise": offre.entreprise.nom,
                "ville": offre.ville,
                "type": offre.type,
                "categorie": offre.get_categorie_display(),
                "profil": offre.profil_recherche[:200],
                "score": score_normalized,
            }
        )

    if offres_data:
        nb = len(offres_data)
        msg = f"J'ai trouvé {nb} offre{'s' if nb > 1 else ''} qui correspond{'ent' if nb > 1 else ''} à votre profil !"
    else:
        msg = "Aucune offre ne correspond exactement, mais essayez d'autres termes."

    return JsonResponse({"offres": offres_data, "message": msg})


def offres_list(request):
    offres = Offre.objects.filter(statut="disponible").order_by("-id")
    return render(request, "offres/list_offres.html", {"offres": offres})


def offre_detail(request, id):
    offre = get_object_or_404(Offre, id=id)

    if request.method == "POST":
        form = CandidatureForm(request.POST, request.FILES)
        if form.is_valid():
            candidature = form.save(commit=False)
            candidature.offre = offre
            candidature.save()
            messages.success(request, "Votre candidature a été envoyée avec succès !")
            return redirect("offre_detail", id=offre.id)
    else:
        form = CandidatureForm()

    return render(request, "offres/offre_detail.html", {"offre": offre, "form": form})


@login_required
def mes_candidatures(request):
    candidatures = Candidature.objects.filter(email=request.user.email).order_by(
        "-date_envoi"
    )
    return render(
        request, "offres/mes_candidatures.html", {"candidatures": candidatures}
    )
