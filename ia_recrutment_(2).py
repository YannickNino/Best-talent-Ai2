import streamlit as st
import os
from PyPDF2 import PdfReader
import google.generativeai as genai
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import matplotlib.pyplot as plt

# Configuration de l'API Google
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Titre de l'application
st.title("📝 Outil de Recrutement Intelligent")

# Section 1 : Rédaction de l'offre d'emploi
st.header("1. Rédiger une offre d'emploi")
offre_texte = st.text_area("Rédigez votre offre d'emploi ici :", height=200)

# Section 2 : Chargement des CVs
st.header("2. Charger les CVs (format PDF)")
uploaded_files = st.file_uploader("Téléchargez les CVs des candidats", type="pdf", accept_multiple_files=True)

if uploaded_files and offre_texte:
    # Traitement des CVs
    contenus_cvs = {}
    for uploaded_file in uploaded_files:
        reader = PdfReader(uploaded_file)
        contenu = ""
        for page in reader.pages:
            contenu += page.extract_text() + "\n"
        contenus_cvs[uploaded_file.name] = contenu

    # Section 3 : Analyse des CVs
    st.header("3. Analyse des CVs")

    # Fonction pour analyser les CVs
    def analyser_cvs(contenus_cvs, offre):
        resultats = []
        for nom_cv, contenu_cv in contenus_cvs.items():
            model = genai.GenerativeModel("gemini-pro")
            prompt = f"Analyse le CV suivant et attribue une note sur 10 en fonction de l'offre d'emploi :\n{offre}\n\nCV :\n{contenu_cv}"
            reponse = model.generate_content(prompt)
            note = reponse.text.strip()
            resultats.append({"nom": nom_cv, "note": float(note.split("/")[0])})  # Extraction de la note
        return resultats

    # Analyse des CVs
    resultats_candidats = analyser_cvs(contenus_cvs, offre_texte)

    # Affichage des résultats sous forme de graphique
    st.subheader("Résultats des candidats")
    noms = [resultat['nom'] for resultat in resultats_candidats]
    notes = [resultat['note'] for resultat in resultats_candidats]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(noms, notes, color="skyblue")
    ax.set_xlabel("Candidats", fontsize=14)
    ax.set_ylabel("Notes", fontsize=14)
    ax.set_title("Notes des candidats en fonction des CV", fontsize=16)
    ax.set_ylim(0, 10)
    plt.xticks(rotation=45, ha="right", fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    st.pyplot(fig)

    # Section 4 : Génération des questions d'entretien
    st.header("4. Questions d'entretien")

    # Fonction pour générer les questions
    def formuler_questions(cv, offre):
        model = genai.GenerativeModel("gemini-pro")
        prompt = f"Génère des questions d'entretien basées sur le CV suivant :\n{cv}\n\nOffre d'emploi :\n{offre}"
        reponse = model.generate_content(prompt)
        return reponse.text.strip()

    # Affichage des questions pour chaque candidat
    for nom_cv, contenu_cv in contenus_cvs.items():
        st.subheader(f"Questions pour {nom_cv}")
        questions = formuler_questions(contenu_cv, offre_texte)
        st.write(questions)

else:
    st.warning("Veuillez rédiger une offre d'emploi et charger les CVs pour continuer.")