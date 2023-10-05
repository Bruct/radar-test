import json
import datetime
import math
import extra_streamlit_components as stx
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
from PIL import Image


#Settings

page_title = "Radar de maturité Data"
page_icon = "img/logo-browser-bar.png"
layout = "centered"
st.set_page_config(page_title=page_title, page_icon= page_icon, layout=layout)
st.markdown(f"<h1 style='text-align: center; color: black;'><b>{page_title}</b></h1>", unsafe_allow_html=True)
left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image('img/Image1.png')


selected = option_menu(
    menu_title=None,
    options=["Radar", "Rechercher", "Comparer"],
    icons=["pencil-fill", "search", "bar-chart-fill"],  
    orientation="horizontal",
    styles = {
        "nav-link-selected": {"background-color": "#503078"},
        "nav-link": {"font-size": "14px"},
    }
)
likert = [
    "Pas du tout d'accord",
    "Pas d'accord",
    "Ni en accord ni en désaccord",
    "D'accord",
    "Tout à fait d'accord"
]
axes = [
    "Axe 1: Gouvernance & Rôles :",
    "Axe 2: Culture & Sensibilisation :",
    "Axe 3: Qualité des données & Stockage :",
    "Axe 4: Outillage & Amélioration continue :",
    "Axe 5: Sécurité, Confidentialité & Conformité :"
]
dico_affirmation = dict()
dico_affirmation[axes[0]] = [
    "Un cadre de gestion des données est clairement défini et documenté",   
    "Le cadre de gouvernance des données est optimal et répond aux besoins de l'entreprise/l'organisation", 
    "Les responsabilités en matière de gestion des données sont bien définies et comprises de tous", 
    "Un propriétaire est clairement défini pour chaque ensemble de données",
    "L'analyse des données conduit à de nouvelles orientations stratégiques",  
    "Vous disposez de toutes les compétences nécessaires pour analyser les données de manière optimale"   
]
dico_affirmation[axes[1]] = [
    "Les collaborateurs sont sensibilisés sur l'importance des données et de leur gestion",   
    "Il existe des formations sur la gestion et l'utilisation des données auprès des collaborateurs pour en tirer pleinement parti", 
    "Les différentes équipes collaborent efficacement pour exploiter les données", 
    "Des processus de partage de connaissances sont mis en place pour partager les bonnes pratiques liées aux données" 
]
dico_affirmation[axes[2]] = [
    "Les données de l'entreprise sont majoritairement fiables",   
    "Des processus de correction d'erreurs de données sont définis et mis en place", 
    "Les données sont mises à jour régulièrement", 
    "Des règles sont mises en place afin de garantir la cohérence des données entre les différents systèmes",
    "Le processus de collecte de données est efficacement géré et documenté",   
    "Les sources de données sont identifiées et évaluées", 
    "Le stockage des données est conforme aux meilleures pratiques du marché", 
    "Il existe des politiques de rétention des données pour gérer leur durée de vie" 
]
dico_affirmation[axes[3]] = [
    "Les infrastructures technologiques/outils sont adaptés pour gérer et analyser les données",   
    "Les outils de gestion des données sont accessibles, documentés et adaptés aux besoins de l'entreprise/l'organisation", 
    "L'infrastructure technologique est suffisamment évolutive pour accompagner la croissance des données", 
    "Il existe un processus d'amélioration continue mis en place pour la gestion des données"
]
dico_affirmation[axes[4]] = [
    "Il existe des processus et/ou règles relatifs à la confidentialité des données et ils sont partagés aux collaborateurs",   
    "Les politiques d'archivage et de suppression des données sont partagées auprès des collaborateurs et appliquées", 
    "Des procédures dédiées sont partagées auprès des collaborateurs et mises en place pour garantir la destruction sécurisée des données obsolètes", 
    "Des règles de sécurité sont définies et mises en place pour assurer la protection des données contre les cyberattaques",
    "Il existe des processus de sauvegarde sécurisés des données de l'entreprise dans le cas d'éventuels sinistres/cyberattaques",   
    "Vous estimez que l'entreprise/l'organisation est en conformité avec les réglementations de protection des données"
]
Axes = ["Gouvernance data", "Culture data", "Qualité de la donnée", "Socle technique", "Réglementaire/Sécuritaire"]
practice_sectorielle = ["Public Sector", "Manufacturing, Energy, Utilities", "Financial Services", "Retail - Luxe", "Transport & Services"]
f = open("questions-reponses.json", "r", encoding="utf-8")
dat = json.load(f)
f.close()

h = open("random-db.json", "r", encoding="utf-8")
test_data = json.load(h)
h.close()
st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #503078;">
  <a class="navbar-brand" href="https://digiplace.sharepoint.com/sites/home/fr-FR" target="_blank">Wavestone</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav"> 
    <ul class="navbar-nav">
      <li class="nav-item active">
        <a class="nav-link disabled" href="#">Home <span class="sr-only">(current)</span></a>
      </li>
    </ul>
  </div>
</nav>
""", unsafe_allow_html=True)
st.markdown("""
    <style>
    .big-font {
        font-size:20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- functions ---

def score_compute(answers):
    gouvernance_data = 0
    culture_data = 0
    qualite_data = 0
    outillage_data = 0
    securite = 0
    for axe, affirmations in answers.items():
        count = 0
        try:
            if axe==axes[0]:
                for affirmation, reponse in affirmations.items():
                    count+=1
                    points = likert.index(reponse)                    
                    gouvernance_data+= points
                gouvernance_data = gouvernance_data/count
            elif axe==axes[1]:
                for affirmation, reponse in affirmations.items():
                    count+=1
                    points = likert.index(reponse)                    
                    culture_data+= points
                culture_data = culture_data/count
            elif axe==axes[2]:
                for affirmation, reponse in affirmations.items():
                    count+=1
                    points = likert.index(reponse)                    
                    qualite_data+= points
                qualite_data = qualite_data/count
            elif axe==axes[3]:
                for affirmation, reponse in affirmations.items():
                    count+=1
                    points = likert.index(reponse)                    
                    outillage_data+= points
                outillage_data = outillage_data/count
            elif axe==axes[4]:
                for affirmation, reponse in affirmations.items():
                    count+=1
                    points = likert.index(reponse)                    
                    securite+= points
                securite = securite/count
        except KeyError:
            pass
    return gouvernance_data, culture_data, qualite_data, outillage_data, securite
        
def find_id_from_name(name):
    for id, dico in test_data.items():
        if dico["nom"]==name:
            return id   

def radar_chart(select):
        scores = list(map(round, list(score_compute(select)), [1 for i in range(5)]))
        fig = px.line_polar(
        {'Maturité':scores, 'Catégorie':['Gouvernance & Rôles','Culture & Sensibilisation',
            'Qualité des données & Stockage', 'Outillage & Amélioration continue', "Sécurité, Confidentialité & Conformité"]}, 
        r="Maturité", 
        theta="Catégorie", 
        start_angle=360,
        line_close=True,
        text="Maturité"
        )
        fig.update_traces(textposition='top center', fill='toself')

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0,4]
                )
            ),
            showlegend=False
        )
        st.write(fig)   

def multiple_charts(first_choice, second_choice):
    first_score = list(map(round, list(score_compute(first_choice)), [1 for i in range(5)]))
    second_score = list(map(round, list(score_compute(second_choice)), [1 for i in range(5)]))
    fig = go.Figure()

    fig = px.line_polar(
    {'Maturité':first_score, 'Entreprise': first_choice["nom"], 'Catégorie':['Gouvernance & Rôles','Culture & Sensibilisation',
            'Qualité des données & Stockage', 'Outillage & Amélioration continue', "Sécurité, Confidentialité & Conformité"]}, 
    r="Maturité", 
    theta="Catégorie", 
    start_angle=360,
    line_close=True,
    text="Maturité",
    hover_name='Entreprise'
    )

    fig2 = px.line_polar(
        {'Maturité':second_score, 'Entreprise': second_choice["nom"], 'Catégorie':['Gouvernance & Rôles','Culture & Sensibilisation',
            'Qualité des données & Stockage', 'Outillage & Amélioration continue', "Sécurité, Confidentialité & Conformité"]}, 
        r="Maturité", 
        color_discrete_sequence=["salmon"]*5,
        theta="Catégorie",
        start_angle=360, 
        line_close=True,
        text="Maturité",
        hover_name='Entreprise'
    )

    ## add fig2 to fig
    fig.add_trace(fig2.data[0])

    fig.update_traces(textposition='top center', fill='toself')

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0,4]
            )
        ),
        showlegend=False
    )

    return fig

def new_index_dict(data_dict):
    max_number = None
    for key in data_dict.keys():
        if key.isdigit():
            key_as_num = int(key)
            if max_number is None or key_as_num > max_number:
                max_number = key_as_num
    return max_number+1 if max_number != None else 0
    
def print_maturity():
    st.markdown("<p class='big-font'>Niveaux de maturité</p>", unsafe_allow_html=True)
    st.image('img/all_numbered.png')
    st.markdown("**Niveau 1 Initial :** L'entreprise/l'organisation n'a pas de cadre de gouvernance instauré. Les données sont gérées de manière ad hoc. Il n'y a pas de processus ni de règles mis en place pour assurer leur qualité, leur suivi, leur sécurité ou leur confidentialité.")
    st.markdown("**Niveau 2 Ad-hoc :** L'entreprise/l'organisation initie et débute la mise en place de processus et d'instances de gouvernance des données. Il n'y a pas de coordination entre les différents départements et les données ne sont pas toujours bien partagées.")
    st.markdown("**Niveau 3 Opérationnel :** L'entreprise/l'organisation a un cadre de gouvernance de données établi et mis en place à l'échelle de l'entreprise. Il existe des processus et des règles pour assurer la qualité, le suivi, la sécurité et la confidentialité des données.")
    st.markdown("**Niveau 4 Optimisé :** L'entreprise/l'organisation s'inscrit dans un processus d'amélioration continue de son cadre de gouvernance mis en place. Des outils sont mis en place afin d'automatiser les processus et améliorer l'efficacité.")
    st.markdown("**Niveau 5 Organisationnel :** L'entreprise/l'organisation est considérée comme très mature en termes de gouvernance des données. Les données sont utilisées pour prendre des décisions stratégiques et participe à la création de nouveaux produits/services.")
    
# --- Main page ---
    
if selected == "Radar":
    placeholder = st.empty()
    with placeholder.form("formulaire"):
        st.markdown("##### Remplir le formulaire ci-dessous pour réaliser votre radar de maturité Data")
        st.header("Fiche de l'entreprise/organisation")
        st.markdown("###### IMPORTANT : Merci de ne pas diffuser le lien du Radar Data à toute personne externe à Wavestone pour des questions de confidentialité concernant les données clients présentes. Par ailleurs, veiller à ne pas indiquer le nom du client dans le cadre d'une mission confidentielle, seulement son secteur d'activité (notamment pour le secteur financier).")
        st.text_area("", placeholder="Renseigner le nom de l'entité ainsi que l'entité groupe", key="nom")
        st.selectbox("Secteur d'activité", practice_sectorielle, key="secteur")
        #st.selectbox("Taille de l'entreprise", ["0-50 employés", "51-500 employés", "501-1000 employés", "1001 à 2000 employés", "+2000 employés"], key="taille")
        st.date_input("Date de mise à jour", datetime.datetime(2023, 10, 1), key="date")
        st.markdown("Consigne : Pour chaque question, cocher une réponse parmi les 5 proposées")
        st.markdown("0. Pas du tout d'accord")
        st.markdown("1. Pas d'accord")
        st.markdown("2. Ni en accord ni en désaccord")
        st.markdown("3. D'accord")
        st.markdown("4. Tout à fait d'accord")
        current_axe = ''
        for axe, affirmations in dico_affirmation.items():
            if current_axe != axe:
                st.header(axe)
                current_axe = axe
            for affirmation in affirmations:   
                st.radio(affirmation, likert, horizontal=False, key=affirmation)
        submitted = st.form_submit_button("Envoyer le formulaire")
        if submitted:
            placeholder.empty()
            st.session_state["submit"]=True
            rep = dict()
            rep["nom"]=st.session_state["nom"]
            rep["secteur"]=st.session_state["secteur"]
            rep["date"]=str(st.session_state["date"])
            for axe, affirmations in dico_affirmation.items():
                if axe not in rep.keys():
                    rep[axe] = dict()
                for affirmation in affirmations:
                    rep[axe][affirmation] = st.session_state[affirmation]
            current_index = str(new_index_dict(test_data))
            test_data[current_index]=rep
    if submitted:
        scores = list(score_compute(rep))
        average_score = sum(scores)/float(len(scores))
        for count,elem in enumerate(axes):
            test_data[current_index]['score'+elem]=scores[count]
        test_data[current_index]["score moyen"] = average_score
        with open("random-db.json", 'w', encoding="utf-8") as outfile:
                json.dump(test_data, outfile, indent=4, ensure_ascii=False)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Nom", rep["nom"])
        col2.metric("Secteur d'activité", rep["secteur"])
        col3.metric("Maturité globale", round(average_score, 1) )
        with col4:
            if average_score<1:
                st.image('img/initial1.png')
            elif average_score<2:
                st.image('img/ad-hoc1.png')
            elif average_score<3:
                st.image('img/operationnel1.png')
            elif average_score<4:
                st.image('img/optimise1.png')    
            elif average_score<5:
                st.image('img/organisationnel1.png')    
        radar_chart(rep)
        print(scores)
        
           
if selected == "Rechercher":
    st.markdown("<p class='big-font'>Rechercher un radar de maturité Data d'une entreprise/organisation</p>", unsafe_allow_html=True)
    data_keys = list(test_data.keys())
    liste_noms_db = []
    for key in data_keys:
        if isinstance(test_data[key], dict):
            liste_noms_db.append(test_data[key]["nom"])
    if liste_noms_db!=[]:
        st.selectbox("Choisir une entreprise/organisation", liste_noms_db, key = "chosen1")
        first_selection = test_data[find_id_from_name(st.session_state["chosen1"])]
        scores = list(score_compute(first_selection))
        average_score = sum(scores)/float(len(scores))
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Nom", first_selection["nom"])
        col2.metric("Secteur d'activité", first_selection["secteur"])
        col3.metric("Maturité globale", round(average_score,1) )
        with col4:
            if average_score<1:
                st.image('img/initial1.png')
            elif average_score<2:
                st.image('img/ad-hoc1.png')
            elif average_score<3:
                st.image('img/operationnel1.png')
            elif average_score<4:
                st.image('img/optimise1.png')    
            elif average_score<5:
                st.image('img/organisationnel1.png')  
        radar_chart(first_selection)
    else:
        st.write("Pas de questionnaire rempli dans la base de données.")
    print_maturity()
if selected == "Comparer":
    # --- Data visualization ---
    st.markdown("<p class='big-font'>Comparer un radar de maturité Data d'une entreprise/organisation par rapport au marché</p>", unsafe_allow_html=True)
    data_keys = list(test_data.keys())
    liste_noms_db = []
    for key in data_keys:
        if isinstance(test_data[key], dict):
            liste_noms_db.append(test_data[key]["nom"])
    if liste_noms_db!=[]:
        st.selectbox("Choisir une entreprise/organisation", liste_noms_db, key = "chosen1")
        first_selection = test_data[find_id_from_name(st.session_state["chosen1"])]

        st.selectbox("Choisir une entreprise/organisation", liste_noms_db, key = "chosen2")
        second_selection = test_data[find_id_from_name(st.session_state["chosen2"])]
        st.plotly_chart(multiple_charts(first_selection, second_selection))
    else:
        st.write("Pas de questionnaire rempli dans la base de données.")
    print_maturity()
    # st.header(":trophy: Leaderboard")
    # st.markdown("Retrouvez ici le TOP 5 des entreprises selon les critères de votre choix")
    # axe_leaderboard = st.selectbox("Axe de maturité souhaité", ["Tout", "Gouvernance data", "Culture data", "Cas d'usage data", "Qualité de la donnée", "Socle technique", "Réglementaire/Sécuritaire"], key="choix leaderboard")
    # secteur_leaderboard = st.selectbox("Secteur de l'entreprise", ["Tout"]+practice_sectorielle, key="choix secteur")
    # taille_leaderboard = st.selectbox("Taille de l'entreprise", ["Tout"]+["0-50 employés", "51-500 employés", "501-1000 employés", "1001 à 2000 employés", "+2000 employés"], key="choix taille")
    # h = open("random-db.json", "r", encoding="utf-8")
    # test_data = json.load(h)
    # h.close()
    # df_data = pd.DataFrame.from_dict(test_data).T
    # df_work = df_data[["nom","score moyen", "secteur", "taille"]+Axes]
    # if secteur_leaderboard != "Tout":
    #     df_work = df_work[df_work["secteur"]==secteur_leaderboard]
    #     df_work.drop("secteur", inplace=True, axis=1)
    # if taille_leaderboard != "Tout":
    #     df_work = df_work[df_work["taille"]==taille_leaderboard]
    #     df_work.drop("taille", inplace=True, axis=1)
    # if axe_leaderboard != "Tout":
    #     df_work = df_work.sort_values(by=axe_leaderboard, ascending=False).iloc[:5,:]
    #     axes_without_choice = Axes
    #     axes_without_choice.remove(axe_leaderboard)
    #     for elem in axes_without_choice:
    #         df_work.drop(elem, inplace=True, axis=1)
    # else:
    #     for elem in Axes:
    #         df_work.drop(elem, inplace=True, axis=1)
    #     df_work = df_work.sort_values(by='score moyen', ascending=False).iloc[:5,:]
    # st.dataframe(df_work.head()) 
    
    
# --- Streamlit style ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
padding = 0
condense_layout = f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """
metric_font = """
<style>
[data-testid="stMetricValue"] {
    font-size: 20px;
}
</style>
"""

st.markdown(metric_font, unsafe_allow_html=True)    
st.markdown(hide_st_style, unsafe_allow_html=True)
st.markdown(condense_layout, unsafe_allow_html=True)
