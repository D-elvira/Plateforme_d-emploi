"""
Remplir la base avec 27 offres réparties sur 5 entreprises.
Usage: python populate_data.py
"""

import os, sys, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plateforme_emploi.settings")
try:
    django.setup()
except RuntimeError:
    pass

from users.models import User
from offres.models import Entreprise, Offre


def run():
    all_usernames = [
        "mtn_cm",
        "orange_cm",
        "totalenergies_cm",
        "afriland_bank",
        "sonatrel_cm",
        "notaire_sarl",
        "agritech_cm",
        "camrail",
        "kiro_games",
        "mtn_cameroun",
        "orange_cameroun",
        "total_energies",
        "kiroo_games",
    ]
    Offre.objects.all().delete()
    Entreprise.objects.filter(user__username__in=all_usernames).delete()
    User.objects.filter(username__in=all_usernames).delete()

    entreprises_data = [
        {
            "username": "mtn_cameroun",
            "email": "recrutement@mtn.cm",
            "password": "Mtn@2026!",
            "nom": "MTN Cameroun",
            "ville": "Douala",
            "domaine": "Télécommunications",
        },
        {
            "username": "orange_cameroun",
            "email": "rh@orange.cm",
            "password": "Orange@2026!",
            "nom": "Orange Cameroun",
            "ville": "Douala",
            "domaine": "Télécommunications & Digital",
        },
        {
            "username": "afriland_bank",
            "email": "carrieres@afrilandfirstbank.com",
            "password": "Afriland@2026!",
            "nom": "Afriland First Bank",
            "ville": "Yaoundé",
            "domaine": "Banque & Finance",
        },
        {
            "username": "total_energies",
            "email": "rh@totalenergies.cm",
            "password": "Total@2026!",
            "nom": "TotalEnergies Cameroun",
            "ville": "Douala",
            "domaine": "Énergie & Pétrole",
        },
        {
            "username": "kiroo_games",
            "email": "jobs@kirogames.cm",
            "password": "Kiroo@2026!",
            "nom": "Kiro'o Games",
            "ville": "Douala",
            "domaine": "Jeux Vidéo & Technologie",
        },
    ]

    entreprises = {}
    for e in entreprises_data:
        user = User.objects.create_user(
            username=e["username"],
            email=e["email"],
            password=e["password"],
            role="recruteur",
        )
        entreprise = Entreprise.objects.create(
            user=user, nom=e["nom"], ville=e["ville"], domaine=e["domaine"]
        )
        entreprises[e["nom"]] = entreprise

    offres_data = [
        # MTN Cameroun (6 offres)
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
            "profil_recherche": "Analyste data capable d'exploiter de grands volumes de données pour générer des insights business. Maîtrise de SQL, Power BI et Python.",
            "attentes": "Bac+4/5 en Statistiques, Data Science ou Informatique. Minimum 1 an d'expérience.",
        },
        {
            "entreprise": "MTN Cameroun",
            "titre": "Chef de Projet IT",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Yaoundé",
            "profil_recherche": "Chef de projet pour coordonner le développement de solutions télécoms innovantes. Gestion des équipes, planification et suivi des livrables.",
            "attentes": "Bac+5 en Informatique ou Gestion de projets. Certification PMP ou Scrum Master appréciée. 3 ans d'expérience.",
        },
        {
            "entreprise": "MTN Cameroun",
            "titre": "Stage en Marketing Digital",
            "type": "stage",
            "categorie": "academique",
            "ville": "Douala",
            "profil_recherche": "Étudiant en marketing ou communication digitale, créatif et à l'aise avec les réseaux sociaux. Connaissance de Canva, Meta Business Suite.",
            "attentes": "Bac+2/3 en Marketing ou Communication. Stage académique de 3 mois.",
        },
        {
            "entreprise": "MTN Cameroun",
            "titre": "Ingénieur Réseau & Télécom",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Douala",
            "profil_recherche": "Ingénieur spécialisé dans les infrastructures réseau et télécommunications. Maîtrise des technologies 4G/5G, fibre optique et solutions cloud.",
            "attentes": "Diplôme d'ingénieur en Télécommunications. 2 ans d'expérience minimum.",
        },
        # Orange Cameroun (6 offres)
        {
            "entreprise": "Orange Cameroun",
            "titre": "Développeur Full Stack (React/Node.js)",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Douala",
            "profil_recherche": "Développeur full stack pour créer des applications web modernes. Maîtrise de React, Node.js, MongoDB et déploiement AWS.",
            "attentes": "Bac+3/5 en Informatique. 2 ans d'expérience. Portfolio de projets web apprécié.",
        },
        {
            "entreprise": "Orange Cameroun",
            "titre": "Stage en Développement Mobile",
            "type": "stage",
            "categorie": "professionnel",
            "ville": "Douala",
            "profil_recherche": "Étudiant passionné par le développement mobile. Connaissance de Flutter ou React Native. Création d'interfaces modernes et performantes.",
            "attentes": "Bac+3/4 en Informatique. Stage de 4 à 6 mois. Motivation et autonomie.",
        },
        {
            "entreprise": "Orange Cameroun",
            "titre": "Responsable Support Client",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Yaoundé",
            "profil_recherche": "Manager pour superviser l'équipe support client. Excellentes aptitudes en communication, gestion d'équipe et résolution de problèmes.",
            "attentes": "Bac+3/5 en Management ou Communication. 3 ans d'expérience en service client.",
        },
        {
            "entreprise": "Orange Cameroun",
            "titre": "Comptable Junior",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Douala",
            "profil_recherche": "Comptable pour gérer les opérations comptables quotidiennes. Maîtrise du plan OHADA, Sage et Excel avancé.",
            "attentes": "Bac+3/4 en Comptabilité ou Finance. 1 an d'expérience. Rigueur exigée.",
        },
        {
            "entreprise": "Orange Cameroun",
            "titre": "Stage en Ressources Humaines",
            "type": "stage",
            "categorie": "academique",
            "ville": "Douala",
            "profil_recherche": "Étudiant en GRH, organisé et communicatif. Participation au recrutement, gestion administrative du personnel.",
            "attentes": "Bac+2/3 en GRH ou Management. Stage académique de 2 à 3 mois.",
        },
        {
            "entreprise": "Orange Cameroun",
            "titre": "UI/UX Designer",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Douala",
            "profil_recherche": "Designer pour concevoir des interfaces intuitives pour nos applications mobiles et web. Maîtrise de Figma, Adobe XD et prototypage.",
            "attentes": "Bac+3 en Design Graphique ou UX Design. Portfolio requis. Sensibilité aux besoins utilisateurs.",
        },
        # Afriland First Bank (5 offres)
        {
            "entreprise": "Afriland First Bank",
            "titre": "Chargé de Clientèle Entreprises",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Yaoundé",
            "profil_recherche": "Chargé de clientèle pour accompagner les entreprises dans leurs besoins financiers. Excellentes compétences relationnelles et connaissance des produits bancaires.",
            "attentes": "Bac+4/5 en Banque, Finance ou Commerce. 2 ans d'expérience en relation client bancaire.",
        },
        {
            "entreprise": "Afriland First Bank",
            "titre": "Stage en Audit Interne",
            "type": "stage",
            "categorie": "professionnel",
            "ville": "Yaoundé",
            "profil_recherche": "Étudiant en audit, comptabilité ou finance, rigoureux et méthodique. Connaissance des normes d'audit et de contrôle interne.",
            "attentes": "Bac+4/5 en Audit ou Comptabilité. Stage professionnel de 6 mois.",
        },
        {
            "entreprise": "Afriland First Bank",
            "titre": "Développeur Mobile (Flutter)",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Yaoundé",
            "profil_recherche": "Développeur mobile pour la création d'applications bancaires innovantes. Maîtrise de Flutter, intégration d'API REST et paiement mobile.",
            "attentes": "Bac+3/5 en Informatique. Portfolio d'applications publiées. 1 an d'expérience minimum.",
        },
        {
            "entreprise": "Afriland First Bank",
            "titre": "Analyste Risque & Conformité",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Douala",
            "profil_recherche": "Analyste pour évaluer les risques opérationnels et financiers. Connaissance des réglementations COBAC et lutte anti-blanchiment.",
            "attentes": "Bac+5 en Finance, Droit ou Économie. 2 ans d'expérience dans le secteur bancaire.",
        },
        {
            "entreprise": "Afriland First Bank",
            "titre": "Stage en Communication Institutionnelle",
            "type": "stage",
            "categorie": "academique",
            "ville": "Yaoundé",
            "profil_recherche": "Étudiant en communication pour participer à la stratégie de communication interne et externe. Rédaction, événementiel et relations presse.",
            "attentes": "Bac+3/4 en Communication ou Journalisme. Bonne plume et créativité. Stage de 3 mois.",
        },
        # TotalEnergies Cameroun (5 offres)
        {
            "entreprise": "TotalEnergies Cameroun",
            "titre": "Ingénieur HSE",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Douala",
            "profil_recherche": "Ingénieur HSE pour superviser la conformité aux normes de sécurité sur les sites industriels. Connaissance des normes ISO 14001.",
            "attentes": "Bac+5 en Génie Industriel ou HSE. 3 ans d'expérience dans le secteur pétrolier.",
        },
        {
            "entreprise": "TotalEnergies Cameroun",
            "titre": "Stage Ingénieur en Géologie",
            "type": "stage",
            "categorie": "professionnel",
            "ville": "Douala",
            "profil_recherche": "Étudiant en géologie, intéressé par l'exploration pétrolière. Compréhension des méthodes sismiques et cartographie géologique.",
            "attentes": "Bac+4/5 en Géologie. Stage de 4 à 6 mois sur site.",
        },
        {
            "entreprise": "TotalEnergies Cameroun",
            "titre": "Comptable Senior",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Douala",
            "profil_recherche": "Comptable expérimenté pour la comptabilité générale et analytique. Maîtrise du plan OHADA et des logiciels SAP, Sage.",
            "attentes": "Bac+4/5 en Comptabilité ou Finance. 5 ans d'expérience. Rigueur et discrétion.",
        },
        {
            "entreprise": "TotalEnergies Cameroun",
            "titre": "Ingénieur Logistique & Supply Chain",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Douala",
            "profil_recherche": "Ingénieur logistique pour optimiser la chaîne d'approvisionnement. Planification, suivi des opérations et gestion des partenaires.",
            "attentes": "Bac+5 en Logistique ou Génie Industriel. 2 ans d'expérience.",
        },
        {
            "entreprise": "TotalEnergies Cameroun",
            "titre": "Stage en Droit des Affaires",
            "type": "stage",
            "categorie": "academique",
            "ville": "Yaoundé",
            "profil_recherche": "Étudiant en droit des affaires pour assister le service juridique. Rédaction de contrats, veille réglementaire et conformité.",
            "attentes": "Bac+4/5 en Droit. Bonne maîtrise de l'anglais. Stage de 3 mois.",
        },
        # Kiro'o Games (5 offres)
        {
            "entreprise": "Kiro'o Games",
            "titre": "Game Designer Junior",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Douala",
            "profil_recherche": "Game designer créatif pour concevoir des mécaniques de jeu innovantes. Maîtrise de Unity ou Unreal Engine, passion pour les jeux vidéo africains.",
            "attentes": "Bac+3 en Game Design ou Informatique. Portfolio de projets personnels ou game jams.",
        },
        {
            "entreprise": "Kiro'o Games",
            "titre": "Stage en Animation 3D",
            "type": "stage",
            "categorie": "professionnel",
            "ville": "Douala",
            "profil_recherche": "Étudiant en animation 3D pour participer à la création de personnages et décors pour nos jeux vidéo.",
            "attentes": "Bac+3/5 en Animation 3D ou Beaux-Arts. Maîtrise de Blender ou Maya. Stage de 4 à 6 mois.",
        },
        {
            "entreprise": "Kiro'o Games",
            "titre": "Développeur Unity C#",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Douala",
            "profil_recherche": "Développeur C# pour le développement de jeux sur Unity. Programmation gameplay, optimisation performance et intégration des assets.",
            "attentes": "Bac+3/5 en Informatique. 1 an d'expérience avec Unity. Passion pour le gaming.",
        },
        {
            "entreprise": "Kiro'o Games",
            "titre": "Community Manager Gaming",
            "type": "emploi",
            "categorie": "poste",
            "ville": "Douala",
            "profil_recherche": "Community manager passionné de jeux vidéo pour animer nos réseaux sociaux et notre communauté de joueurs. Création de contenu engageant.",
            "attentes": "Bac+2/3 en Communication ou Marketing. Expérience en gestion de communauté gaming.",
        },
        {
            "entreprise": "Kiro'o Games",
            "titre": "Stage en Développement Web",
            "type": "stage",
            "categorie": "academique",
            "ville": "Douala",
            "profil_recherche": "Étudiant en informatique pour développer et maintenir notre site web vitrine. HTML, CSS, JavaScript et notions de Django.",
            "attentes": "Bac+2/3 en Informatique. Stage académique de 2 à 3 mois. Motivation et curiosité.",
        },
    ]

    for o in offres_data:
        Offre.objects.create(
            entreprise=entreprises[o["entreprise"]],
            titre=o["titre"],
            type=o["type"],
            categorie=o["categorie"],
            ville=o["ville"],
            profil_recherche=o["profil_recherche"],
            attentes=o["attentes"],
            statut="disponible",
        )

    print(f"\n{'='*55}")
    print(f"  {Offre.objects.count()} offres creees avec succes !")
    print(f"  {Entreprise.objects.count()} entreprises en base")
    print(f"{'='*55}")
    print(f"\n  COMPTES RECRUTEURS :")
    print(f"  {'─'*50}")
    for e in entreprises_data:
        print(f"  {e['nom']}")
        print(f"    Login:    {e['username']}")
        print(f"    Mot de passe: {e['password']}")
        print(f"    Email:    {e['email']}")
        print()


if __name__ == "__main__":
    run()
