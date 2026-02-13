
# --------------------
# IMPORTS
# --------------------

import streamlit as st
from streamlit_authenticator import Authenticate
from streamlit_option_menu import option_menu
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Mon Application", layout="wide")

# --------------------
# FONCTIONS VOTES
# --------------------

VOTES_FILE = "votes.csv"

def init_votes_file():
    if not os.path.exists(VOTES_FILE):
        pd.DataFrame(columns=["timestamp", "personnage", "camp"]).to_csv(VOTES_FILE, index=False)

def add_vote(personnage, camp):
    init_votes_file()
    new_row = pd.DataFrame([{
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "personnage": personnage,
        "camp": camp
    }])
    new_row.to_csv(VOTES_FILE, mode="a", header=False, index=False)

def load_votes():
    init_votes_file()
    return pd.read_csv(VOTES_FILE)

def reset_votes():
    if os.path.exists(VOTES_FILE):
        os.remove(VOTES_FILE)
    init_votes_file()

# --------------------
# DONNÉES UTILISATEURS
# --------------------

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

authenticator = Authenticate(
    lesDonneesDesComptes,
    "cookie_name",
    "cookie_key",
    30,
)

authenticator.login()

def accueil():
    st.title("Bienvenue dans la guerre des étoiles !")

# --------------------
# APPLICATION
# --------------------

#SI CONNECTÉ
if st.session_state.get("authentication_status"):

    # ---- SIDEBAR (UNIQUEMENT CONNECTÉ) ----
    with st.sidebar:
        st.write(f"Bienvenue {st.session_state.get('name')} 👋")
        authenticator.logout("Déconnexion")  # ✅ ici seulement

        selection = option_menu(
            menu_title="Menu",
            options=["Accueil", "Personnages", "Votes", "Album"],
            icons=["house", "people", "check2-square", "image"],
            default_index=0
        )

        add_selectbox = st.selectbox(
            "Quel est ton personnage préféré",
            ("Obiwan Kenobi", "Dark Vador", "Luke Skywalker", "Yoda", "R2D2", "C3PO",
             "Chewbacca", "Han Solo", "Padmé Amidala", "Anakin Skywalker", "Palpatine", "Maitre Windu")
        )

        add_radio = st.radio(
            "Choisis ton camp",
            ("Côté Obscur", "Côté Lumineux")
        )

    # ---- PAGES ----
    if selection == "Accueil":
        accueil()
        st.write("Bienvenue sur le côté Obscur de la Force !")
        st.write("ID: ObiwanKenobi / Password: Laforce")
        st.image("Images/Star_Wars_Logo.svg.png")

    elif selection == "Personnages":
        st.header("Présentation des personnages de la saga Star Wars")
        st.write(
            "Découvrez les personnages emblématiques de la saga Star Wars, des héros courageux aux méchants redoutables. "
            "Plongez dans l'univers fascinant de la galaxie lointaine, très lointaine, et explorez les histoires captivantes "
            "de ces personnages légendaires."
        )

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

        choix = st.selectbox("Choisis un personnage", list(personnages.keys()))
        st.subheader(choix)
        st.image(personnages[choix]["img"], use_container_width=True)
        st.write(personnages[choix]["texte"])
    
    elif selection == "Votes":
        st.header("🗳️ Votes galactiques")

        # ✅ choix depuis la sidebar
        perso_vote = add_selectbox
        camp_vote = add_radio  # déjà "Côté Obscur" ou "Côté Lumineux"

        # --- bouton vote
        if st.button("🔥 Valider mon vote", use_container_width=True):
            add_vote(perso_vote, camp_vote)
            st.success("Vote enregistré. Que la Force soit avec toi.")
            st.rerun()

        # --- stats
        df_votes = load_votes()

        total = len(df_votes)
        obscur = int((df_votes["camp"] == "Côté Obscur").sum()) if total > 0 else 0
        lumineux = int((df_votes["camp"] == "Côté Lumineux").sum()) if total > 0 else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("Total votes", total)
        col2.metric("Côté Obscur", obscur)
        col3.metric("Côté Lumineux", lumineux)

        st.divider()

        # --- Classement personnages
        st.subheader("🏆 Classement des personnages")
        if total == 0:
            st.info("Aucun vote pour le moment.")
        else:
            classement = df_votes["personnage"].value_counts().reset_index()
            classement.columns = ["Personnage", "Votes"]

            top3 = classement.head(3)
            st.write("### Top 3")
            for i, row in top3.iterrows():
                medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
                st.write(f"{medal} **{row['Personnage']}** — {row['Votes']} votes")

            st.divider()
            st.bar_chart(classement.set_index("Personnage")["Votes"])

        st.divider()

        # --- Répartition camps
        st.subheader("⚖️ Répartition des camps")
        if total > 0:
            camps_count = df_votes["camp"].value_counts()
            st.bar_chart(camps_count)

        st.markdown("---")

        # --- Reset (admin)
        if st.button("🔄 Reset des votes (Admin uniquement)"):
            if st.session_state.get("username") == "DarkVador":
                reset_votes()
                st.warning("Les archives ont été effacées par le côté Obscur ☠️")
                st.rerun()
            else:
                st.error("Seul l'Empereur peut effacer les archives.")


    elif selection == "Album":
        st.header("📸 Album Galactique")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.image("Images/Obiwan_Kenobi.jpg", caption="Obiwan Kenobi", use_container_width=True)
        with col2:
            st.image("Images/DarkVador.jpg", caption="Dark Vador", use_container_width=True)
        with col3:
            st.image("Images/Luke_Skywalker.jpg", caption="Luke Skywalker", use_container_width=True)

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
elif st.session_state.get("authentication_status") is False:
    st.error("L'username ou le password est incorrect.")

# SI RIEN SAISI
else:
    st.warning("Veuillez entrer l'username et le mot de passe : ObiwanKenobi / Laforce")
