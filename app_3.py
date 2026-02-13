# --------------------
# IMPORTS
# --------------------

import streamlit as st
from streamlit_authenticator import Authenticate
from streamlit_option_menu import option_menu
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Mon Application", layout="wide")     # pour un affichage en plein écran

# --------------------
# FONCTIONS VOTES
# --------------------

VOTES_FILE = "votes.csv"                                            # fichier pour stocker les votes (dans le même dossier que ce script)

# Assure que le fichier de votes existe, sinon le crée avec les bonnes colonnes :
def init_votes_file():                                       
    if not os.path.exists(VOTES_FILE):                             
        pd.DataFrame(columns=["timestamp", "personnage", "camp"]).to_csv(VOTES_FILE, index=False)

# Ajoute un vote au fichier CSV :
def add_vote(personnage, camp):
    init_votes_file()                                               # s'assure que le fichier existe avant d'ajouter un vote
    new_row = pd.DataFrame([{                                       # crée une nouvelle ligne de données à ajouter
        "timestamp": datetime.now().isoformat(timespec="seconds"),  # enregistre la date et l'heure du vote
        "personnage": personnage,                                   # enregistre le personnage choisi
        "camp": camp                                                # enregistre le camp choisi (Côté Obscur ou Côté Lumineux)
    }])
    new_row.to_csv(VOTES_FILE, mode="a", header=False, index=False) # ajoute la nouvelle ligne au fichier CSV sans réécrire les en-têtes

def load_votes():                                                   # charge les votes depuis le fichier CSV, en s'assurant que le fichier existe d'abord
    init_votes_file()                                               # s'assure que le fichier existe avant de tenter de le charger
    return pd.read_csv(VOTES_FILE)                                  # charge les données du fichier CSV dans un DataFrame pandas et le retourne
def reset_votes():                                                 # supprime le fichier de votes s'il existe, puis le recrée vide (utilisé pour réinitialiser les votes)
    if os.path.exists(VOTES_FILE):                                  # vérifie si le fichier de votes existe avant de tenter de le supprimer
        os.remove(VOTES_FILE)                                       # supprime le fichier de votes pour effacer tous les votes enregistrés
    init_votes_file()                                               

# --------------------
# DONNÉES UTILISATEURS
# --------------------

# Les données des comptes utilisateurs sont stockées dans un dictionnaire. 
# Chaque utilisateur a un nom, un mot de passe, une adresse e-mail, un compteur de tentatives de connexion échouées, un statut de connexion et un rôle (utilisateur ou administrateur).
lesDonneesDesComptes = {
    'usernames': {
        'ObiwanKenobi': {
            'name': 'ObiwanKenobi',
            'password': 'Laforce',
            'email': 'utilisateur@gmail.com',
            'failed_login_attemps': 0,
            'logged_in': False,
            'role': 'utilisateur'
        },
        'DarkVador': {
            'name': 'Dark Vador',
            'password': "L'empire",
            'email': 'admin@gmail.com',
            'failed_login_attemps': 0,
            'logged_in': False,
            'role': 'administrateur'
        }
    }
}

# Crée une instance de l'authentificateur en utilisant les données des comptes. 
# Les paramètres "cookie_name" et "cookie_key" sont utilisés pour gérer les cookies de session, et le dernier paramètre (30) indique la durée de validité des cookies en minutes.
authenticator = Authenticate(
    lesDonneesDesComptes,
    "cookie_name",
    "cookie_key",
    30,
)
# Affiche le formulaire de connexion et gère l'authentification. Si les identifiants sont corrects, l'utilisateur est connecté et peut accéder à l'application. Sinon, un message d'erreur est affiché.
authenticator.login()

def accueil():
    st.title("Bienvenue dans la guerre des étoiles !")

# --------------------
# APPLICATION
# --------------------

#Si "CONNECTÉ"
if st.session_state.get("authentication_status"):

    # ---- SIDEBAR (UNIQUEMENT CONNECTÉ) ----
    with st.sidebar:
        st.write(f"Bienvenue {st.session_state.get('name')} 👋")               
        authenticator.logout("Déconnexion")  
        # Le menu de navigation dans la sidebar permet à l'utilisateur de choisir entre différentes pages de l'application. Chaque option est accompagnée d'une icône.
        selection = option_menu(                   
            menu_title="Menu",
            options=["Accueil", "Personnages", "Votes", "Album"],
            icons=["house", "people", "check2-square", "image"],
            default_index=0                                                                       #Par défaut, la page "Accueil" est sélectionnée.
        )
        # Les éléments suivants dans la sidebar permettent à l'utilisateur de participer à un vote en choisissant son personnage préféré parmi une liste déroulante. 
        add_selectbox = st.selectbox(
            "Quel est ton personnage préféré",
            ("Obiwan Kenobi", "Dark Vador", "Luke Skywalker", "Yoda", "R2D2", "C3PO",
             "Chewbacca", "Han Solo", "Padmé Amidala", "Anakin Skywalker", "Palpatine", "Maitre Windu")
        )
        # Le bouton radio "Choisis ton camp" permet à l'utilisateur de sélectionner s'il préfère le Côté Obscur ou le Côté Lumineux, ce qui sera également pris en compte lors de l'enregistrement des votes.
        add_radio = st.radio(
            "Choisis ton camp",
            ("Côté Obscur", "Côté Lumineux")
        )

    # ---- LES PAGES ----
    # En fonction de la sélection de l'utilisateur dans le menu de navigation, différentes sections de l'application sont affichées. 
    if selection == "Accueil":
        accueil()
        st.write("Bienvenue sur le côté Obscur de la Force !")
        st.write("ID: ObiwanKenobi / Password: Laforce")
        st.image("Images/Star_Wars_Logo.svg.png")
    # La section "Personnages" affiche une présentation des personnages, accompagnée d'une description de chacun d'eux. 
    elif selection == "Personnages":
        st.header("Présentation des personnages de la saga Star Wars")
        st.write(
            "Découvrez les personnages emblématiques de la saga Star Wars, des héros courageux aux méchants redoutables. "
            "Plongez dans l'univers fascinant de la galaxie lointaine, très lointaine, et explorez les histoires captivantes "
            "de ces personnages légendaires."
        )
        # Les données des personnages sont stockées dans un dictionnaire, où chaque clé est le nom du personnage et la valeur est un autre dictionnaire contenant l'URL de l'image et le texte descriptif.
        personnages = {
            "Obiwan Kenobi": {
                "img": "Images/Obiwan_Kenobi.jpg",
                "texte": "Obi-Wan Kenobi avance comme une lame calme. Maître Jedi, gardien d’un équilibre fragile, il porte la discipline comme une armure — et la compassion comme une faille assumée."
            },
            "Dark Vador": {
                "img": "Images/DarkVador.jpg",
                "texte": "Dark Vador ne marche pas : il s’impose. Chaque respiration est un écho du passé. Il a aimé, il a chuté… et dans l’ombre qu’il a embrassée, il cherche encore une rédemption."
            },
            "Luke Skywalker": {
                "img": "Images/Luke_Skywalker.jpg",
                "texte": "Luke Skywalker est l’étincelle improbable. Un garçon du désert qui refuse d’abandonner. Il prouve qu’un héritage ne définit pas un destin — le choix, oui."
            },
            "Yoda": {
                "img": "Images/Yoda.jpg",
                "texte": "Yoda parle peu, mais chaque mot pèse. Gardien de la sagesse millénaire, il sait que la Force n’est ni lumière ni obscurité — mais équilibre."
            },
            "R2D2": {
                "img": "Images/R2D2.jpg",
                "texte": "Petit droïde au courage immense. R2-D2 ne brandit pas de sabre laser, mais sans lui, les héros seraient souvent perdus. Fidèle, ingénieux, indispensable."
            },
            "C3PO": {
                "img": "Images/C3PO.jpg",
                "texte": "C-3PO connaît six millions de formes de communication… mais peine encore à comprendre le chaos humain. Peureux parfois, loyal toujours."
            },
            "Chewbacca": {
                "img": "Images/Chewbacca.jpg",
                "texte": "Chewbacca est une force brute guidée par un cœur immense. Derrière chaque rugissement se cache une loyauté inébranlable."
            },
            "Han Solo": {
                "img": "Images/Han_Solo.jpg",
                "texte": "Han Solo se prétend mercenaire, mais agit en héros. Cynique en façade, noble au fond. Il choisit toujours le bon camp — même quand il prétend le contraire."
            },
            "Padmé Amidala": {
                "img": "Images/Padme_Amidala.jpg",
                "texte": "Padmé Amidala combat sans sabre laser. Diplomate brillante, elle croit en la République quand tout vacille. Son courage est silencieux, mais décisif."
            },
            "Anakin Skywalker": {
                "img": "Images/Anakin_Skywalker.jpg",
                "texte": "Anakin Skywalker est la promesse et la tragédie. Puissant au-delà de toute mesure, il cherche à vaincre la peur… et finit par en devenir l’esclave."
            },
            "Palpatine": {
                "img": "Images/Palpatine.jpg",
                "texte": "Palpatine ne conquiert pas par la force brute, mais par la patience. Stratège de l’ombre, il manipule les événements jusqu’à ce que la galaxie plie."
            },
            "Maitre Windu": {
                "img": "Images/Maitre_Windu.jpg",
                "texte": "Maître Windu incarne la rigueur absolue. Maîtrisant le Vaapad, il flirte avec l’ombre sans s’y perdre. Une autorité rare, une puissance redoutable."
            }
        }
        # L'utilisateur peut sélectionner un personnage dans une liste déroulante pour voir son image et sa description détaillée.
        choix = st.selectbox("Choisis un personnage", list(personnages.keys()))
        st.subheader(choix)
        st.image(personnages[choix]["img"], use_container_width=True)
        st.write(personnages[choix]["texte"])
    # La section "Votes" permet aux utilisateurs de voter pour leur personnage préféré et affiche les statistiques des votes. 
    elif selection == "Votes":
        st.header("Votes galactiques")

        # choix depuis la sidebar
        perso_vote = st.selectbox("Choisis ton personnage préféré", list(personnages.keys()))          # permet à l'utilisateur de sélectionner son personnage parmi une liste déroulante, en utilisant les clés du dictionnaire "personnages" pour afficher les options disponibles.
        camp_vote = st.radio("Choisis ton camp", ["Côté Obscur", "Côté Lumineux"])                     # permet à l'utilisateur de choisir son camp préféré à l'aide d'un bouton radio, ce qui sera également pris en compte lors de l'enregistrement des votes.

        # --- bouton vote
        # Lorsque l'utilisateur clique sur le bouton "Valider mon vote", la fonction "add_vote" est appelée pour enregistrer le vote dans le fichier CSV. 
        if st.button("🔥 Valider mon vote", use_container_width=True):                                    
            add_vote(perso_vote, camp_vote)                 
            st.success("Vote enregistré. Que la Force soit avec toi !")                                 # Un message de succès est affiché pour informer l'utilisateur que son vote a été enregistré, et la page est rechargée pour refléter les changements.
            st.rerun()

        # --- stats
        # On charge les votes depuis le fichier CSV pour calculer les statistiques. Le nombre total de votes est calculé, ainsi que le nombre de votes pour chaque camp.
        df_votes = load_votes()

        total = len(df_votes)                                                            # nombre total de votes enregistrés dans le DataFrame
        obscur = int((df_votes["camp"] == "Côté Obscur").sum()) if total > 0 else 0      # nombre de votes pour le Côté Obscur, calculé en filtrant le DataFrame pour les lignes où la colonne "camp" est égale à "Côté Obscur" et en sommant les résultats. Si le total de votes est zéro, on évite la division par zéro en retournant 0.
        lumineux = int((df_votes["camp"] == "Côté Lumineux").sum()) if total > 0 else 0  # nombre de votes pour le Côté Lumineux, calculé de la même manière que pour le Côté Obscur, mais en filtrant pour les lignes où la colonne "camp" est égale à "Côté Lumineux". Si le total de votes est zéro, on retourne également 0 pour éviter la division par zéro.
        # Les statistiques des votes sont affichées à l'aide de la fonction "metric" de Streamlit, qui permet de présenter des chiffres clés de manière visuellement attrayante. 
        col1, col2, col3 = st.columns(3)                                                 # création de trois colonnes pour afficher les statistiques des votes
        col1.metric("Total votes", total)                                                # affichage du nombre total de votes dans la première colonne
        col2.metric("Côté Obscur", obscur)                                               # affichage du nombre de votes pour le Côté Obscur dans la deuxième colonne
        col3.metric("Côté Lumineux", lumineux)                                           # affichage du nombre de votes pour le Côté Lumineux dans la troisième colonne
        
        st.divider()                                                                     # ligne de séparation pour une meilleure organisation visuelle de la page

        # --- Classement personnages
        # Le classement des personnages est affiché en utilisant la fonction "value_counts" de pandas pour compter le nombre de votes pour chaque personnage. 
        # Les résultats sont présentés dans un DataFrame, qui est ensuite affiché à l'aide de la fonction "bar_chart" de Streamlit pour visualiser le classement des personnages en fonction du nombre de votes reçus.
        st.subheader("🏆 Classement des personnages")              
        if total == 0:
            st.info("Aucun vote pour le moment.")
        else:
            classement = df_votes["personnage"].value_counts().reset_index()
            classement.columns = ["Personnage", "Votes"]
            
            top3 = classement.head(3)
            st.write("### Top 3")
            for i, row in top3.iterrows():                                              # boucle sur les trois premiers personnages du classement pour afficher leur position, leur nom et le nombre de votes reçus. Un emoji de médaille est utilisé pour différencier les trois premiers : 🥇 pour le premier, 🥈 pour le deuxième et 🥉 pour le troisième.
                medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
                st.write(f"{medal} **{row['Personnage']}** — {row['Votes']} votes")     # affichage du classement des trois premiers personnages avec leur position, leur nom et le nombre de votes reçus, accompagné d'un emoji de médaille pour différencier les trois premiers.

            st.divider()                                                                # ligne de séparation pour une meilleure organisation visuelle de la page
            st.bar_chart(classement.set_index("Personnage")["Votes"])                   # affichage du classement complet des personnages sous forme de graphique à barres, où l'axe des x représente les personnages et l'axe des y représente le nombre de votes reçus. Le DataFrame est réindexé pour que les noms des personnages soient utilisés comme index, et la colonne "Votes" est sélectionnée pour être affichée dans le graphique à barres.

        st.divider()                                                                    # ligne de séparation pour une meilleure organisation visuelle de la page

        # --- Répartition camps
        st.subheader("⚖️ Répartition des votes par camp")                                       
        if total > 0:                                                                   # si des votes ont été enregistrés, la répartition des camps est affichée à l'aide de la fonction "value_counts" de pandas pour compter le nombre de votes pour chaque camp. Les résultats sont présentés dans un DataFrame, qui est ensuite affiché à l'aide de la fonction "bar_chart" de Streamlit pour visualiser la répartition des camps en fonction du nombre de votes reçus.
            camps_count = df_votes["camp"].value_counts()                               # comptage du nombre de votes pour chaque camp (Côté Obscur et Côté Lumineux) en utilisant la fonction "value_counts" de pandas sur la colonne "camp" du DataFrame des votes
            st.bar_chart(camps_count)                                                   # affichage de la répartition des camps sous forme de graphique à barres, où l'axe des x représente les camps (Côté Obscur et Côté Lumineux) et l'axe des y représente le nombre de votes reçus pour chaque camp. Le DataFrame "camps_count" est utilisé pour alimenter le graphique à barres.

        st.markdown("---")

        # --- Bouton reset (admin)
        # Un bouton de réinitialisation des votes est disponible uniquement pour l'administrateur (Dark Vador). Lorsque ce bouton est cliqué, la fonction "reset_votes" est appelée pour supprimer tous les votes enregistrés dans le fichier CSV. Un message d'avertissement est affiché pour informer que les archives ont été effacées, et la page est rechargée pour refléter les changements. Si un utilisateur qui n'est pas l'administrateur tente de cliquer sur ce bouton, un message d'erreur est affiché pour indiquer que seul l'Empereur peut effacer les archives.
        if st.button("🔄 Reset des votes (Admin uniquement)"):                  
            if st.session_state.get("username") == "DarkVador":
                reset_votes()
                st.warning("Les archives ont été effacées par le côté Obscur ☠️")
                st.rerun()
            else:
                st.error("Seul l'Empereur peut effacer les archives.")

    # La section "Album" présente une galerie d'images des personnages emblématiques de la saga Star Wars. Les images sont organisées en plusieurs lignes, avec trois images par ligne, et chaque image est accompagnée d'une légende indiquant le nom du personnage représenté.
    elif selection == "Album":
        st.header("📸 Album Galactique")
    # La section "Album" présente une galerie d'images des personnages emblématiques de la saga Star Wars. Les images sont organisées en plusieurs lignes, avec trois images par ligne, et chaque image est accompagnée d'une légende indiquant le nom du personnage représenté.
        col1, col2, col3 = st.columns(3)                                                                     # création de trois colonnes pour organiser les images en ligne
        with col1:                                                                                           # utilisation d'un bloc "with" pour la première colonne, permettant d'afficher une image avec une légende dans cette colonne
            st.image("Images/Obiwan_Kenobi.jpg", caption="Obiwan Kenobi", use_container_width=True)          # affichage de l'image d'Obiwan Kenobi avec une légende et en utilisant toute la largeur du conteneur de la colonne
        with col2:                                                                                           # utilisation d'un bloc "with" pour la deuxième colonne, permettant d'afficher une image avec une légende dans cette colonne
            st.image("Images/DarkVador.jpg", caption="Dark Vador", use_container_width=True)                 # affichage de l'image de Dark Vador avec une légende et en utilisant toute la largeur du conteneur de la colonne
        with col3:                                                                                           # utilisation d'un bloc "with" pour la troisième colonne, permettant d'afficher une image avec une légende dans cette colonne
            st.image("Images/Luke_Skywalker.jpg", caption="Luke Skywalker", use_container_width=True)        # affichage de l'image de Luke Skywalker avec une légende et en utilisant toute la largeur du conteneur de la colonne

        col1, col2, col3 = st.columns(3)
        with col1:
            st.image("Images/Yoda.jpg", caption="Yoda", use_container_width=True)
        with col2:
            st.image("Images/R2D2.jpg", caption="R2D2", use_container_width=True)
        with col3:
            st.image("Images/C3PO.jpg", caption="C3PO", use_container_width=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.image("Images/Chewbacca.jpg", caption="Chewbacca", use_container_width=True)
        with col2:
            st.image("Images/Han_Solo.jpg", caption="Han Solo", use_container_width=True)
        with col3:
            st.image("Images/Padme_Amidala.jpg", caption="Padmé Amidala", use_container_width=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.image("Images/Anakin_Skywalker.jpg", caption="Anakin Skywalker", use_container_width=True)
        with col2:
            st.image("Images/Palpatine.jpg", caption="Palpatine", use_container_width=True)
        with col3:
            st.image("Images/Maitre_Windu.jpg", caption="Maitre Windu", use_container_width=True)

# SI MAUVAIS IDENTIFIANTS
# Si les identifiants de connexion sont incorrects, un message d'erreur est affiché pour informer l'utilisateur que l'username ou le password est incorrect. 
elif st.session_state.get("authentication_status") is False:
    st.error("L'username ou le password est incorrect.")

# SI RIEN SAISI
# Si aucun identifiant n'est saisi, un message d'avertissement est affiché pour inviter l'utilisateur à entrer les informations de connexion correctes. 
else:
    st.warning("Veuillez entrer l'username et le mot de passe : ObiwanKenobi / Laforce")
