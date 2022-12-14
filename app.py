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

page_title = "Audit de maturité 360° - Data Gouvernance"
page_icon = "https://www.wavestone.com/app/uploads/2016/06/E_WAVESTONE_Profil-Twitter_400x400.png"
layout = "centered"

st.set_page_config(page_title=page_title, page_icon= page_icon, layout=layout)
st.title(page_title )
#st.text("Retrouvez sur l'onglet formulaire, un formulaire à remplir pour ajouter une \nentreprise ou une entité d'une entreprise dans la base de données.")
#   st.text("Vous pourrez ensuite visualiser et comparer l'évaluation de maturité de différentes\nentreprises en cliquant sur l'onglet Radar de maturité.")


selected = option_menu(
    menu_title=None,
    options=["Audit", "Entreprises", "Comparaison", "Méthodologie"],
    icons=["pencil-fill", "card-list", "bar-chart-fill", "search"],  
    orientation="horizontal",
    styles = {
        "nav-link": {"font-size": "14px"},
    }
)
Axes = ["Gouvernance data", "Culture data", "Cas d'usage data", "Qualité de la donnée", "Socle technique", "Réglementaire/Sécuritaire"]
practice_sectorielle = ["Public sector", "Manufacturing, energy, utilities", "Financial Services", "Retail - Luxe", "Transport & services"]
f = open("questions-reponses.json", "r", encoding="utf-8")
dat = json.load(f)
f.close()

h = open("random-db.json", "r", encoding="utf-8")
test_data = json.load(h)
h.close()


# --- functions ---

def score_compute(answers):
    gouvernance_data = 0
    culture_data = 0
    cas_usage_data = 0
    qualite_data = 0
    socle_technique = 0
    reglementaire = 0
    for i in answers.keys():
        try:
            if dat[i]["thème"]=="Gouvernance data":
                gouvernance_data+= 4*dat[i]["reponses"][answers[i]]/22
            elif dat[i]["thème"]=="Culture data":
                culture_data+= 4*dat[i]["reponses"][answers[i]]/22
            elif dat[i]["thème"]=="Cas d'usage data":
                cas_usage_data+= 4*dat[i]["reponses"][answers[i]]/21
            elif dat[i]["thème"]=="Qualité de la donnée":
                qualite_data+= 4*dat[i]["reponses"][answers[i]]/9
            elif dat[i]["thème"]=="Socle technique":
                socle_technique+= 4*dat[i]["reponses"][answers[i]]/14
            elif dat[i]["thème"]=="Réglementaire/Sécuritaire":
                reglementaire+= 4*dat[i]["reponses"][answers[i]]/13
        except KeyError:
            pass
    return gouvernance_data, culture_data, cas_usage_data, qualite_data, socle_technique, reglementaire
        
def find_id_from_name(name):
    for id, dico in test_data.items():
        if dico["nom"]==name:
            return id   

def radar_chart(select):
        scores = list(map(round, list(score_compute(select)), [1 for i in range(6)]))
        fig = px.line_polar(
        {'Maturité':scores, 'Catégorie':['Governance data','Culture data','Cas d\'usages data',
            'Qualité de la donnée', 'Socle technique', "Réglementaire/Sécuritaire"]}, 
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
    first_score = list(map(round, list(score_compute(first_choice)), [1 for i in range(6)]))
    second_score = list(map(round, list(score_compute(second_choice)), [1 for i in range(6)]))
    fig = go.Figure()

    fig = px.line_polar(
    {'Maturité':first_score, 'Entreprise': first_choice["nom"], 'Catégorie':['Governance data','Culture data','Cas d\'usages data',
            'Qualité de la donnée', 'Socle technique', "Réglementaire/Sécuritaire"]}, 
    r="Maturité", 
    theta="Catégorie", 
    start_angle=360,
    line_close=True,
    text="Maturité",
    hover_name='Entreprise'
    )

    fig2 = px.line_polar(
        {'Maturité':second_score, 'Entreprise': second_choice["nom"], 'Catégorie':['Governance data','Culture data','Cas d\'usages data',
            'Qualité de la donnée', 'Socle technique', "Réglementaire/Sécuritaire"]}, 
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

def metric_box(bold_text, wch_colour_box, small_text="", line_height=22.70, border_width=0):
    wch_colour_font = (0,0,0)
    fontsize = 18
    iconname = "fa-solid fa-ranking-star"
    htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                                {wch_colour_box[1]}, 
                                                {wch_colour_box[2]}, 0.75); 
                            color: rgb({wch_colour_font[0]}, 
                                    {wch_colour_font[1]}, 
                                    {wch_colour_font[2]}, 0.75); 
                            font-size: {fontsize}px;
                            border-color: black;
                            border-width: {border_width}px;
                            border-style: solid; 
                            border-radius: 7px; 
                            padding-left: 12px; 
                            padding-top: 18px; 
                            padding-bottom: 18px; 
                            line-height:{line_height}px;'>
                            <i class='{iconname} fa-xs'></i> {bold_text}
                            </style><BR><span style='font-size: 14px; 
                            margin-top: 0;'>{small_text}</style></span></p>"""
    return htmlstr
    
# --- Main page ---

if selected=="Méthodologie":
    #st.markdown("""Pour évaluer au mieux votre maturité en termes de gouvernance de données nous avons élaboré un formulaire
    #            permettant d'avoir une vision 360° de l'état de la gouvernance des données au sein de votre entreprise.""")
    st.header("Méthodologie du radar")
    st.subheader("1. Critères d'évaluation")
    st.text("Niveaux de maturité possibles:")
    dic_maturite = {0: ["Sujet non abordé", (231, 0, 35), 0], 1: ["Initial", (251,135,58), 0], 2:["Partiellement mature", (251,235,46), 0], 3:["Mature", (82,198,125), 0], 4:["Amélioration continue", (32,168,117), 0]}
    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v6.2.0/css/all.css" crossorigin="anonymous">'
    htmlstr0 = metric_box(dic_maturite[0][0], dic_maturite[0][1], line_height=36, border_width = dic_maturite[0][2]) 
    htmlstr1 = metric_box(dic_maturite[1][0], dic_maturite[1][1], small_text="Exploratoire & non structuré", border_width = dic_maturite[1][2])
    htmlstr2 = metric_box(dic_maturite[2][0], dic_maturite[2][1], small_text="Structuré & non industrialisé", line_height = 14, border_width = dic_maturite[2][2])
    htmlstr3 = metric_box(dic_maturite[3][0], dic_maturite[3][1], small_text="Structuré & industrialisé", border_width = dic_maturite[3][2])
    htmlstr4 = metric_box(dic_maturite[4][0], dic_maturite[4][1], line_height=24, border_width = dic_maturite[4][2])
    second_col0, second_col1, second_col2, second_col3, second_col4 = st.columns(5)
    second_col0.write(lnk + htmlstr0, unsafe_allow_html=True)
    second_col1.write(lnk + htmlstr1, unsafe_allow_html=True)
    second_col2.write(lnk + htmlstr2, unsafe_allow_html=True)
    second_col3.write(lnk + htmlstr3, unsafe_allow_html=True)
    second_col4.write(lnk + htmlstr4, unsafe_allow_html=True)
    #st.markdown("""
    #            0. **Immature**
    #            1. **Initial** 
    #            2. **Partiellement maîtrisé** 
    #            3. **Maitrisé** 
    #            4. **Mature** 
    #            """)
    st.subheader("2. Axes d'étude")
    st.markdown("""
                6 axes évalués dans l'audit 360°:
                * Gouvernance data
                * Culture data
                * Cas d'usage data
                * Qualité de la donnée 
                * Socle technique
                * Réglementaire/Sécuritaire
                """)
    image = Image.open('grille.png')
    st.image(image, caption='Grille de lecture du radar')
    
    
if selected == "Audit":
    st.markdown("##### Veuillez remplir le formulaire ci-dessous pour réaliser votre audit de maturité 360°")
    placeholder = st.empty()
    with placeholder.form("formulaire"):
        st.header("Fiche d'identité de l'entreprise")
        st.header("IMPORTANT : Veillez à ne pas indiquer le nom du client dans le cadre d'une mission confidentielle ou du secteur financier; indiquez uniquement son secteur d'activité")
        st.text_area("", placeholder="Nom du client", key="nom")
        st.selectbox("Secteur d'activité", practice_sectorielle, key="secteur")
        st.selectbox("Taille de l'entreprise", ["0-50 employés", "51-500 employés", "501-1000 employés", "1001 à 2000 employés", "+2000 employés"], key="taille")
        st.date_input("Date de mise à jour", datetime.datetime(2022, 11, 1), key="date")
        theme = dat["0"]["thème"]
        sous_theme = dat["0"]["sous-thème"]
        st.header(theme)
        st.subheader(sous_theme)
        for i, question_dico in dat.items():
            if question_dico["sous-thème"]!= sous_theme:
                with st.expander("Commentaires"):
                    comment = st.text_area("", placeholder="Commentaires: Spécifiez les bonnes pratiques mises en place chez le client justifiant la réponse", key = "commentaire: "+ question_dico["sous-thème"])
            if question_dico["thème"]!= theme:
                theme = question_dico["thème"]
                st.header(theme)
            if question_dico["sous-thème"]!= sous_theme:
                sous_theme =  question_dico["sous-thème"]
                st.subheader(sous_theme)
            #st.selectbox(question_dico["question"], question_dico["reponses"].keys(), key = i)
            st.radio(question_dico["question"], question_dico["reponses"].keys(), horizontal=False, key = i)
        with st.expander("Commentaires"):
            comment = st.text_area("", placeholder="Commentaires ou justifications", key="commentaire"+question_dico["sous-thème"])
        submitted = st.form_submit_button("Envoyer le formulaire")
        if submitted:
            placeholder.empty()
            st.session_state["submit"]=True
            rep = dict()
            rep["nom"]=st.session_state["nom"]
            rep["secteur"]=st.session_state["secteur"]
            rep["taille"]=st.session_state["taille"]
            rep["date"]=str(st.session_state["date"])
            for question in dat.keys():
                rep[question] = st.session_state[question]
            c = int(list(test_data.keys())[-1])
            c+=1
            test_data[str(c)]=rep
    if submitted:
        scores = list(score_compute(rep))
        average_score = sum(scores)/float(len(scores))
        for count,elem in enumerate(Axes):
            test_data[elem]=scores[count]
        test_data["score moyen"]=average_score
        with open("random-db.json", 'w', encoding="utf-8") as outfile:
                json.dump(test_data, outfile, indent=4, ensure_ascii=False)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Nom", rep["nom"])
        col2.metric("Secteur d'activité", rep["secteur"])
        col3.metric("Taille de l'entreprise", rep["taille"])
        col4.metric("Maturité globale", round(average_score, 1) )
        dic_maturite = {0: ["Sujet non abordé", (231, 0, 35), 0], 1: ["Initial", (251,135,58), 0], 2:["Partiellement mature", (251,235,46), 0], 3:["Mature", (82,198,125), 0], 4:["Amélioration continue", (32,168,117), 0]}
        lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v6.2.0/css/all.css" crossorigin="anonymous">'
        dic_maturite[math.floor(average_score)][2]=2
        htmlstr0 = metric_box(dic_maturite[0][0], dic_maturite[0][1], line_height=36, border_width = dic_maturite[0][2]) 
        htmlstr1 = metric_box(dic_maturite[1][0], dic_maturite[1][1], small_text="Exploratoire & non structuré", border_width = dic_maturite[1][2])
        htmlstr2 = metric_box(dic_maturite[2][0], dic_maturite[2][1], small_text="Structuré & non industrialisé", line_height = 13, border_width = dic_maturite[2][2])
        htmlstr3 = metric_box(dic_maturite[3][0], dic_maturite[3][1], small_text="Structuré & industrialisé", border_width = dic_maturite[3][2])
        htmlstr4 = metric_box(dic_maturite[4][0], dic_maturite[4][1], border_width = dic_maturite[4][2])
        second_col0, second_col1, second_col2, second_col3, second_col4 = st.columns(5)
        second_col0.write(lnk + htmlstr0, unsafe_allow_html=True)
        second_col1.write(lnk + htmlstr1, unsafe_allow_html=True)
        second_col2.write(lnk + htmlstr2, unsafe_allow_html=True)
        second_col3.write(lnk + htmlstr3, unsafe_allow_html=True)
        second_col4.write(lnk + htmlstr4, unsafe_allow_html=True)
        radar_chart(rep)
        print(scores)
        
           
if selected == "Entreprises":
    st.markdown("**Recherchez l'audit de maturité d'une entreprise en particulier**")
    liste_noms_db = [test_data[l]["nom"] for l in test_data.keys()]   
    st.selectbox("Veuillez choisir une entreprise", liste_noms_db, key = "chosen1")
    first_selection = test_data[find_id_from_name(st.session_state["chosen1"])]
    scores = list(score_compute(first_selection))
    average_score = sum(scores)/float(len(scores))
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Nom", first_selection["nom"])
    col2.metric("Secteur d'activité", first_selection["secteur"])
    col3.metric("Taille de l'entreprise", first_selection["taille"])
    col4.metric("Maturité globale", round(average_score,1) )

    dic_maturite = {0: ["Sujet non abordé", (231, 0, 35), 0], 1: ["Initial", (251,135,58), 0], 2:["Partiellement mature", (251,235,46), 0], 3:["Mature", (82,198,125), 0], 4:["Amélioration continue", (32,168,117), 0]}
    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v6.2.0/css/all.css" crossorigin="anonymous">'
    dic_maturite[math.floor(average_score)][2]=2
    htmlstr0 = metric_box(dic_maturite[0][0], dic_maturite[0][1], line_height=36, border_width = dic_maturite[0][2]) 
    htmlstr1 = metric_box(dic_maturite[1][0], dic_maturite[1][1], small_text="Exploratoire & non structuré", border_width = dic_maturite[1][2])
    htmlstr2 = metric_box(dic_maturite[2][0], dic_maturite[2][1], small_text="Structuré & non industrialisé", line_height = 13, border_width = dic_maturite[2][2])
    htmlstr3 = metric_box(dic_maturite[3][0], dic_maturite[3][1], small_text="Structuré & industrialisé", border_width = dic_maturite[3][2])
    htmlstr4 = metric_box(dic_maturite[4][0], dic_maturite[4][1], border_width = dic_maturite[4][2])
    second_col0, second_col1, second_col2, second_col3, second_col4 = st.columns(5)
    second_col0.write(lnk + htmlstr0, unsafe_allow_html=True)
    second_col1.write(lnk + htmlstr1, unsafe_allow_html=True)
    second_col2.write(lnk + htmlstr2, unsafe_allow_html=True)
    second_col3.write(lnk + htmlstr3, unsafe_allow_html=True)
    second_col4.write(lnk + htmlstr4, unsafe_allow_html=True)
    radar_chart(first_selection)
    print(scores)
       
if selected == "Comparaison":
    # --- Data visualization ---
    st.markdown("**Comparez deux audits de maturité 360° d'entreprise**")
    liste_noms_db = [test_data[l]["nom"] for l in test_data.keys()]   
    st.selectbox("Veuillez choisir une entreprise", liste_noms_db, key = "chosen1")
    first_selection = test_data[find_id_from_name(st.session_state["chosen1"])]

    st.selectbox("Veuillez choisir une entreprise", liste_noms_db, key = "chosen2")
    second_selection = test_data[find_id_from_name(st.session_state["chosen2"])]
    st.plotly_chart(multiple_charts(first_selection, second_selection))
    
    st.header(":trophy: Leaderboard")
    st.markdown("Retrouvez ici le TOP 5 des entreprises selon les critères de votre choix")
    axe_leaderboard = st.selectbox("Axe de maturité souhaité", ["Tout", "Gouvernance data", "Culture data", "Cas d'usage data", "Qualité de la donnée", "Socle technique", "Réglementaire/Sécuritaire"], key="choix leaderboard")
    secteur_leaderboard = st.selectbox("Secteur de l'entreprise", ["Tout"]+practice_sectorielle, key="choix secteur")
    taille_leaderboard = st.selectbox("Taille de l'entreprise", ["Tout"]+["0-50 employés", "51-500 employés", "501-1000 employés", "1001 à 2000 employés", "+2000 employés"], key="choix taille")
    h = open("random-db.json", "r", encoding="utf-8")
    test_data = json.load(h)
    h.close()
    df_data = pd.DataFrame.from_dict(test_data).T
    df_work = df_data[["nom","score moyen", "secteur", "taille"]+Axes]
    if secteur_leaderboard != "Tout":
        df_work = df_work[df_work["secteur"]==secteur_leaderboard]
    if taille_leaderboard != "Tout":
        df_work = df_work[df_work["taille"]==taille_leaderboard]
    if axe_leaderboard != "Tout":
        df_work = df_work.sort_values(by=axe_leaderboard, ascending=False).iloc[:5,:]
    else:
        df_work = df_work.sort_values(by='score moyen   ', ascending=False).iloc[:5,:]
    st.dataframe(df_work.head()) 
    
    
    
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
