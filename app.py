# ============================================================
# APP Presse Hermès - Carnet Presse / Communiqués / Événements
# ============================================================
#
# Objectif :
#  Une application simple (via Streamlit) pour gérer :
#    1️⃣ Un carnet de presse (journalistes & influenceurs)
#    2️⃣ L'envoi de communiqués
#    3️⃣ La planification d'événements et une to-do list
#
# Technologies utilisées :
#   - Python (langage)
#   - Streamlit (interface web)
#   - pandas (gestion des données dans des fichiers CSV)
#
# Auteur : toi (avec un coup de pouce 😉)
# ============================================================

# === 1) IMPORTER LES LIBRAIRIES NECESSAIRES ===
import streamlit as st       # pour créer l'interface web
import pandas as pd          # pour gérer les fichiers CSV
from datetime import datetime  # pour ajouter automatiquement la date du jour
import os                    # pour vérifier si les fichiers existent déjà


# === 2) CREER OU LIRE LES FICHIERS CSV SI BESOIN ===
def charger_ou_creer_csv(nom_fichier, colonnes):
    """
    Vérifie si un fichier CSV existe déjà.
    - S'il existe, on le lit et on le renvoie sous forme de DataFrame (tableau)
    - S'il n'existe pas, on le crée vide avec les colonnes nécessaires
    """
    if os.path.exists(nom_fichier):
        return pd.read_csv(nom_fichier)  # on lit le fichier existant
    else:
        df_vide = pd.DataFrame(columns=colonnes)  # on crée un tableau vide
        df_vide.to_csv(nom_fichier, index=False)  # on l'enregistre
        return df_vide


# === 3) CHARGER LES DONNEES AU DEMARRAGE ===
# On définit les colonnes pour chaque fichier CSV
carnet = charger_ou_creer_csv(
    "carnet_presse.csv",
    ["nom", "media", "email", "telephone", "type", "specialite", "notes"]
)

communiques = charger_ou_creer_csv(
    "communiques.csv",
    ["nom_contact", "communique", "date_envoi"]
)

evenements = charger_ou_creer_csv(
    "evenements.csv",
    ["evenement", "tache", "statut", "rsvp"]
)


# === 4) INTERFACE PRINCIPALE AVEC MENU LATERAL ===
st.title("🧡 Application Presse Hermès")

# Menu latéral pour naviguer entre les sections
menu = st.sidebar.radio(
    "Choisir une section :",
    ["Carnet Presse", "Envoi des Communiqués", "Événements & To-do"]
)


# ============================================================
# PAGE 1 : CARNET PRESSE
# ============================================================
if menu == "Carnet Presse":
    st.header("📰 Gérer le carnet presse")

    # --- Formulaire pour ajouter un contact ---
    st.subheader("Ajouter un nouveau contact")
    with st.form("ajout_contact"):
        nom = st.text_input("Nom du journaliste ou influenceur")
        media = st.text_input("Média ou réseau")
        email = st.text_input("Email")
        telephone = st.text_input("Téléphone")
        type_contact = st.selectbox("Type", ["journaliste", "influenceur"])
        specialite = st.text_input("Spécialité (mode, luxe...)")
        notes = st.text_area("Notes")
        ajouter = st.form_submit_button("Ajouter ce contact")

    # Quand on clique sur le bouton "Ajouter"
    if ajouter:
        # On crée une nouvelle ligne (sous forme de dictionnaire)
        nouveau_contact = {
            "nom": nom,
            "media": media,
            "email": email,
            "telephone": telephone,
            "type": type_contact,
            "specialite": specialite,
            "notes": notes
        }
        # On ajoute cette ligne dans le DataFrame
        carnet = pd.concat([carnet, pd.DataFrame([nouveau_contact])], ignore_index=True)
        # On enregistre le fichier CSV mis à jour
        carnet.to_csv("carnet_presse.csv", index=False)
        st.success(f"✅ Contact {nom} ajouté avec succès !")

    # --- Afficher et rechercher dans le carnet ---
    st.subheader("Rechercher ou filtrer")
    recherche_nom = st.text_input("Rechercher par nom")
    filtre_type = st.selectbox("Filtrer par type", ["tous", "journaliste", "influenceur"])

    df_affichage = carnet.copy()
    # Filtrer par nom si une recherche est faite
    if recherche_nom:
        df_affichage = df_affichage[df_affichage["nom"].str.contains(recherche_nom, case=False, na=False)]
    # Filtrer par type si demandé
    if filtre_type != "tous":
        df_affichage = df_affichage[df_affichage["type"] == filtre_type]

    st.dataframe(df_affichage)  # afficher le tableau filtré


# ============================================================
# PAGE 2 : ENVOI DES COMMUNIQUES
# ============================================================
elif menu == "Envoi des Communiqués":
    st.header("✉️ Suivre l'envoi des communiqués de presse")

    # --- Ajouter un envoi ---
    st.subheader("Nouvel envoi de communiqué")
    with st.form("ajout_communique"):
        contact = st.selectbox("Choisir un contact", carnet["nom"].unique())
        communique_nom = st.text_input("Nom du communiqué (ex : Lancement nouveau parfum)")
        date = st.date_input("Date d'envoi", datetime.today())
        ajouter_communique = st.form_submit_button("Enregistrer l'envoi")

    if ajouter_communique:
        nouvel_envoi = {
            "nom_contact": contact,
            "communique": communique_nom,
            "date_envoi": date
        }
        communiques = pd.concat([communiques, pd.DataFrame([nouvel_envoi])], ignore_index=True)
        communiques.to_csv("communiques.csv", index=False)
        st.success(f"✅ Communiqué '{communique_nom}' enregistré pour {contact}")

    # --- Afficher l'historique des envois ---
    st.subheader("Historique des communiqués envoyés")
    st.dataframe(communiques)


# ============================================================
# PAGE 3 : EVENEMENTS & TO-DO LIST
# ============================================================
elif menu == "Événements & To-do":
    st.header("📅 Planifier et suivre les événements")

    # --- Ajouter une tâche ou un événement ---
    st.subheader("Ajouter un événement ou une tâche")
    with st.form("ajout_evenement"):
        evenement_nom = st.text_input("Nom de l'événement")
        tache = st.text_input("Tâche à accomplir")
        statut = st.selectbox("Statut", ["à faire", "fait"])
        rsvp = st.selectbox("RSVP", ["à confirmer", "oui", "non"])
        ajouter_evenement = st.form_submit_button("Ajouter")

    if ajouter_evenement:
        nouvelle_tache = {
            "evenement": evenement_nom,
            "tache": tache,
            "statut": statut,
            "rsvp": rsvp
        }
        evenements = pd.concat([evenements, pd.DataFrame([nouvelle_tache])], ignore_index=True)
        evenements.to_csv("evenements.csv", index=False)
        st.success(f"✅ Tâche '{tache}' ajoutée pour l'événement '{evenement_nom}'")

    # --- Afficher et mettre à jour les tâches ---
    st.subheader("Liste des tâches et événements")
    st.dataframe(evenements)

    # Optionnel : pour aller plus loin on pourrait ajouter un bouton
    # pour changer le statut directement (ex: cocher "fait")