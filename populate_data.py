"""
Script pour remplir la base de données avec 27 offres d'emploi et de stage.
Usage: python manage.py shell < populate_data.py
Ou:    python populate_data.py  (si lancé comme script standalone)
"""

import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plateforme_emploi.settings")

try:
    django.setup()
except RuntimeError:
    pass

from users.models import User
from offres.models import Entreprise, Offre, DA


def run():
    entreprises_data = [
        {
            "username": "mtn_cm",
            "email": "rh@mtn.cm",
            "nom": "MTN Cameroun",
            "ville": "Douala",
            "domaine": "Télécommunications",
        },
        {
            "username": "orange_cm",
            "email": "recrutement@orange.cm",
            "nom": "Orange Cameroun",
            "ville": "Douala",
            "domaine": "Télécommunications",
        },
        {
            "username": "totalenergies_cm",
            "email": "rh@totalenergies.cm",
            "nom": "TotalEnergies Cameroun",
            "ville": "Douala",
            "domaine": "Énergie & Pétrole",
        },
        {
            "username": "afriland_bank",
            "email": "carrieres@afrilandfirstbank.com",
            "nom": "Afriland First Bank",
            "ville": "Yaoundé",
            "domaine": "Banque & Finance",
        },
        {
            "username": "sonatrel_cm",
            "email": "recrutement@sonatrel.cm",
            "nom": "SONATREL",
            "ville": "Yaoundé",
            "domaine": "Énergie & Électricité",
        },
        {
            "username": "notaire_sarl",
            "email": "contact@notaire-digital.cm",
            "nom": "Notaire Digital SARL",
            "ville": "Yaoundé",
            "domaine": "Services Juridiques",
        },
        {
            "username": "agritech_cm",
            "email": "rh@agritech.cm",
            "nom": "AgriTech Solutions",
            "ville": "Bafoussam",
            "domaine": "Agriculture & Technologies",
        },
        {
            "username": "camrail",
            "email": "rh@camrail.net",
            "nom": "Camrail",
            "ville": "Douala",
            "domaine": "Transport Ferroviaire",
        },
        {
            "username": "kiro_games",
            "email": "jobs@kirogames.cm",
            "nom": "Kiro'o Games",
            "ville": "Douala",
            "domaine": "Jeux Vidéo & Technologie",
        },
    ]

    entreprises = {}
    for e in entreprises_data:
        user, created = User.objects.get_or_create(
            username=e["username"], defaults={"email": e["email"], "role": "recruteur"}
        )
        if created:
            user.set_password("Plateforme2026!")
        user.save()

        entreprise, _ = Entreprise.objects.get_or_create(
            user=user,
            defaults={"nom": e["nom"], "ville": e["ville"], "domaine": e["domaine"]},
        )
        entreprises[e["nom"]] = entreprise

    offres_data = [
        {
            "entreprise": "MTN Cameroun",
            "titre": "Développeur Backend Python/Django",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Douala",
            "profil_recherche": "Développeur expérimenté maîtrisant Python, Django et les API REST. Minimum 2 ans d'expérience en développement web. Connaissance des bases de données PostgreSQL et des outils CI/CD.",
            "attentes": "Bac+3/5 en Informatique, expérience avec Git, Docker, tests unitaires. Capacité à travailler en équipe Agile.",
        },
        {
            "entreprise": "MTN Cameroun",
            "titre": "Stage en Cybersécurité",
            "type": "stage",
            "categorie": "professionnel",
            "ville": "Douala",
            "profil_recherche": "Étudiant en sécurité informatique ou réseaux, passionné par la cybersécurité. Connaissance des protocoles réseau TCP/IP, notions de pentesting.",
            "attentes": "En cours de formation Bac+4/5 en sécurité informatique. Stage de 6 mois avec possibilité d'embauche.",
        },
        {
            "entreprise": "MTN Cameroun",
            "titre": "Analyste Data & Business Intelligence",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Douala",
            "profil_recherche": "Analyste data capable d'exploiter de grands volumes de données pour générer des insights business. Maîtrise de SQL, Power BI et Python pour l'analyse de données.",
            "attentes": "Bac+4/5 en Statistiques, Data Science ou Informatique. Minimum 1 an d'expérience en analyse de données.",
        },
        {
            "entreprise": "Orange Cameroun",
            "titre": "Chef de Projet Digital",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Douala",
            "profil_recherche": "Chef de projet digital avec expérience en gestion de projets web et mobile. Capacité à coordonner des équipes techniques et à gérer les délais et budgets.",
            "attentes": "Bac+5 en Gestion de projets ou Informatique. 3 ans d'expérience minimum. Certification PMP ou Scrum Master appréciée.",
        },
        {
            "entreprise": "Orange Cameroun",
            "titre": "Stage en Marketing Digital",
            "type": "stage",
            "categorie": "academique",
            "ville": "Douala",
            "profil_recherche": "Étudiant en marketing ou communication digitale, créatif et à l'aise avec les réseaux sociaux. Connaissance de Canva, Meta Business Suite et Google Analytics.",
            "attentes": "Bac+2/3 en Marketing, Communication ou équivalent. Stage académique de 3 mois.",
        },
        {
            "entreprise": "Orange Cameroun",
            "titre": "Ingénieur Réseau & Télécom",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Yaoundé",
            "profil_recherche": "Ingénieur spécialisé dans les infrastructures réseau et télécommunications. Maîtrise des technologies 4G/5G, fibre optique et solutions cloud.",
            "attentes": "Diplôme d'ingénieur en Télécommunications. 2 ans d'expérience minimum dans le secteur télécom.",
        },
        {
            "entreprise": "TotalEnergies Cameroun",
            "titre": "Ingénieur HSE (Hygiène, Sécurité, Environnement)",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Douala",
            "profil_recherche": "Ingénieur HSE pour superviser la conformité aux normes de sécurité sur les sites industriels. Connaissance des normes ISO 14001 et OHSAS 18001.",
            "attentes": "Bac+5 en Génie industriel ou HSE. Minimum 3 ans d'expérience dans le secteur pétrolier ou industriel.",
        },
        {
            "entreprise": "TotalEnergies Cameroun",
            "titre": "Stage Ingénieur en Géologie Pétrolière",
            "type": "stage",
            "categorie": "professionnel",
            "ville": "Douala",
            "profil_recherche": "Étudiant en géologie ou géosciences, intéressé par l'exploration pétrolière. Bonne compréhension des méthodes sismiques et de la cartographie géologique.",
            "attentes": "En cours de formation Bac+4/5 en Géologie. Stage de 4 à 6 mois sur site.",
        },
        {
            "entreprise": "TotalEnergies Cameroun",
            "titre": "Comptable Senior",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Douala",
            "profil_recherche": "Comptable expérimenté pour gérer la comptabilité générale et analytique. Maîtrise du plan comptable OHADA et des logiciels SAP, Sage.",
            "attentes": "Bac+4/5 en Comptabilité ou Finance. 5 ans d'expérience minimum. Rigueur et discrétion exigées.",
        },
        {
            "entreprise": "Afriland First Bank",
            "titre": "Chargé de Clientèle Entreprises",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Yaoundé",
            "profil_recherche": "Chargé de clientèle pour accompagner les entreprises dans leurs besoins financiers. Excellentes compétences relationnelles et connaissance des produits bancaires.",
            "attentes": "Bac+4/5 en Banque, Finance ou Commerce. 2 ans d'expérience en relation client dans le secteur bancaire.",
        },
        {
            "entreprise": "Afriland First Bank",
            "titre": "Stage en Audit Interne",
            "type": "stage",
            "categorie": "professionnel",
            "ville": "Yaoundé",
            "profil_recherche": "Étudiant en audit, comptabilité ou finance, rigoureux et méthodique. Connaissance des normes d'audit et de contrôle interne.",
            "attentes": "Bac+4/5 en Audit, Comptabilité. Stage professionnel de 6 mois.",
        },
        {
            "entreprise": "Afriland First Bank",
            "titre": "Développeur Mobile (Flutter/React Native)",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Yaoundé",
            "profil_recherche": "Développeur mobile pour la création d'applications bancaires innovantes. Maîtrise de Flutter ou React Native, intégration d'API REST et paiement mobile.",
            "attentes": "Bac+3/5 en Informatique. Portfolio d'applications mobiles publiées. 1 an d'expérience minimum.",
        },
        {
            "entreprise": "SONATREL",
            "titre": "Ingénieur Électricien",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Yaoundé",
            "profil_recherche": "Ingénieur en génie électrique pour la planification et maintenance des réseaux de transport d'électricité haute tension.",
            "attentes": "Diplôme d'ingénieur en Génie Électrique. 2 ans d'expérience dans le secteur énergétique.",
        },
        {
            "entreprise": "SONATREL",
            "titre": "Stage en Gestion des Ressources Humaines",
            "type": "stage",
            "categorie": "academique",
            "ville": "Yaoundé",
            "profil_recherche": "Étudiant en GRH ou Management, organisé et communicatif. Participation au recrutement, gestion administrative du personnel et formation.",
            "attentes": "Bac+2/3 en GRH ou Management. Stage académique de 2 à 3 mois.",
        },
        {
            "entreprise": "SONATREL",
            "titre": "Technicien en Maintenance Industrielle",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Douala",
            "profil_recherche": "Technicien qualifié pour la maintenance préventive et corrective des équipements industriels de transport d'énergie électrique.",
            "attentes": "BTS ou DUT en Maintenance Industrielle ou Électromécanique. 1 an d'expérience minimum.",
        },
        {
            "entreprise": "Notaire Digital SARL",
            "titre": "Développeur Full Stack (Django/React)",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Yaoundé",
            "profil_recherche": "Développeur full stack pour une plateforme de services juridiques en ligne. Maîtrise de Django, React, PostgreSQL et déploiement cloud.",
            "attentes": "Bac+3/5 en Informatique. Expérience avec les architectures microservices. Autonome et proactif.",
        },
        {
            "entreprise": "Notaire Digital SARL",
            "titre": "Stage en Droit du Numérique",
            "type": "stage",
            "categorie": "professionnel",
            "ville": "Yaoundé",
            "profil_recherche": "Étudiant en droit spécialisé dans le numérique ou la cyberjustice. Recherche et rédaction d'articles juridiques sur la transformation digitale.",
            "attentes": "Bac+4/5 en Droit. Intérêt prononcé pour les technologies. Stage de 4 mois.",
        },
        {
            "entreprise": "Notaire Digital SARL",
            "titre": "UI/UX Designer",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Yaoundé",
            "profil_recherche": "Designer UI/UX pour concevoir des interfaces intuitives et modernes pour notre plateforme juridique. Maîtrise de Figma, Adobe XD et prototypage.",
            "attentes": "Bac+3 en Design Graphique ou UX Design. Portfolio de projets web/mobile. Sensibilité aux besoins utilisateurs.",
        },
        {
            "entreprise": "AgriTech Solutions",
            "titre": "Ingénieur Agronome - Projets IoT",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Bafoussam",
            "profil_recherche": "Ingénieur agronome pour piloter des projets d'agriculture de précision utilisant l'IoT. Gestion de capteurs, analyse de données agricoles, formation des agriculteurs.",
            "attentes": "Bac+5 en Agronomie ou Génie Rural. Connaissance des technologies IoT et des systèmes embarqués.",
        },
        {
            "entreprise": "AgriTech Solutions",
            "titre": "Stage en Développement Web",
            "type": "stage",
            "categorie": "academique",
            "ville": "Bafoussam",
            "profil_recherche": "Étudiant en informatique pour participer au développement de notre plateforme de suivi agricole. HTML, CSS, JavaScript et notions de Django.",
            "attentes": "Bac+2/3 en Informatique. Stage académique de 2 à 3 mois. Motivation et curiosité.",
        },
        {
            "entreprise": "AgriTech Solutions",
            "titre": "Commercial Terrain - Solutions Agricoles",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Bafoussam",
            "profil_recherche": "Commercial dynamique pour promouvoir nos solutions technologiques auprès des coopératives agricoles de l'Ouest Cameroun.",
            "attentes": "Bac+2/3 en Commerce ou Marketing. Permis de conduire B. Connaissance du milieu agricole camerounais appréciée.",
        },
        {
            "entreprise": "Camrail",
            "titre": "Ingénieur Logistique & Transport",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Douala",
            "profil_recherche": "Ingénieur logistique pour optimiser les flux de transport ferroviaire de marchandises. Planification, suivi des opérations et gestion des partenaires.",
            "attentes": "Bac+5 en Logistique, Transport ou Génie Industriel. 2 ans d'expérience dans le transport ou la supply chain.",
        },
        {
            "entreprise": "Camrail",
            "titre": "Stage en Communication Institutionnelle",
            "type": "stage",
            "categorie": "professionnel",
            "ville": "Douala",
            "profil_recherche": "Étudiant en communication pour participer à la stratégie de communication interne et externe. Rédaction, événementiel et relations presse.",
            "attentes": "Bac+3/4 en Communication ou Journalisme. Bonne plume et créativité. Stage de 4 à 6 mois.",
        },
        {
            "entreprise": "Camrail",
            "titre": "Mécanicien Ferroviaire",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Douala",
            "profil_recherche": "Mécanicien spécialisé dans la maintenance et la réparation de matériel roulant ferroviaire. Diagnostic des pannes et entretien préventif.",
            "attentes": "CAP/BEP/BTS en Mécanique ou Maintenance. Expérience en milieu industriel souhaitée.",
        },
        {
            "entreprise": "Kiro'o Games",
            "titre": "Game Designer Junior",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Douala",
            "profil_recherche": "Game designer créatif pour concevoir des mécaniques de jeu innovantes. Maîtrise de Unity ou Unreal Engine, passion pour les jeux vidéo africains.",
            "attentes": "Bac+3 en Game Design, Informatique ou Multimédia. Portfolio de projets personnels ou game jams.",
        },
        {
            "entreprise": "Kiro'o Games",
            "titre": "Stage en Animation 3D",
            "type": "stage",
            "categorie": "professionnel",
            "ville": "Douala",
            "profil_recherche": "Étudiant en animation 3D ou arts numériques pour participer à la création de personnages et décors pour nos jeux vidéo.",
            "attentes": "En formation Bac+3/5 en Animation 3D, Multimédia ou Beaux-Arts. Maîtrise de Blender ou Maya. Stage de 4 à 6 mois.",
        },
        {
            "entreprise": "Kiro'o Games",
            "titre": "Développeur Unity C#",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Douala",
            "profil_recherche": "Développeur C# pour le développement de jeux sur Unity. Programmation gameplay, optimisation performance et intégration des assets.",
            "attentes": "Bac+3/5 en Informatique. 1 an d'expérience avec Unity. Passion pour le gaming et la culture africaine.",
        },
    ]

    created_count = 0
    for o in offres_data:
        entreprise = entreprises[o["entreprise"]]
        _, created = Offre.objects.get_or_create(
            entreprise=entreprise,
            titre=o["titre"],
            defaults={
                "type": o["type"],
                "categorie": o["categorie"],
                "ville": o["ville"],
                "profil_recherche": o["profil_recherche"],
                "attentes": o["attentes"],
                "statut": "disponible",
            },
        )
        if created:
            created_count += 1

    print(f"\n{'='*50}")
    print(f"  {created_count} offres créées avec succès !")
    print(f"  {Entreprise.objects.count()} entreprises en base")
    print(f"  {Offre.objects.count()} offres au total")
    print(f"{'='*50}")


if __name__ == "__main__":
    run()
