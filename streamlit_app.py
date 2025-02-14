import streamlit as st
import os
import matplotlib.pyplot as plt
from langchain_core.prompts import ChatPromptTemplate
from PyPDF2 import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

# Configuration de l'API Google
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

@st.cache_resource
def get_model():
    from langchain_google_genai import ChatGoogleGenerativeAI
    return ChatGoogleGenerativeAI(model="gemini-2.0-flash")

model = get_model()

# Titre principal
st.header('📝 BEST-TALENT-AI')

# Entrée des besoins
besoins = st.text_area("Entrez vos besoins ici :", placeholder="Entrez vos besoins pour rédiger une offre...")

@st.cache_data
def generer_offre(besoins):
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", "À partir des informations suivantes, rédige une offre d'emploi complète et bien structurée :\n[besoins]"),
            ("user", "{input}")
        ]
    )
    response = model.invoke(prompt_template.invoke({"input": besoins}))
    return response

if besoins:
    offre = generer_offre(besoins)
    st.write(offre.content)

uploaded_files = st.file_uploader(
    "Choisissez des fichiers de CV (PDF)", accept_multiple_files=True
)

# Extraction des contenus des CV
contenus = {}
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("Fichier chargé :", uploaded_file.name)

    reader = PdfReader(uploaded_file)
    contenu = ""
    for page in reader.pages:
        contenu += page.extract_text() + "\n"
    contenus[uploaded_file.name] = contenu

# Classe pour analyser les CVs
class Info(BaseModel):
    name: str = Field(description="Nom du candidat")
    note: int = Field(description="Note du CV du candidat en fonction de l'offre")

tagging_prompt = ChatPromptTemplate.from_template(
    """
    Analyse le contenu suivant, extrait le nom du candidat et attribue une note sur 10 en fonction de l'offre suivante :\n
    Offre :\n{offre}\n
    CV :\n{cv}\n
    Ne retourne que les informations définies dans la classe Info.
    """
)

llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-2.0-flash").with_structured_output(Info)

@st.cache_data
def analyser_cvs(contenus, offre):
    resultats = []
    for nom_cv, contenu_cv in contenus.items():
        prompt = tagging_prompt.invoke({"offre": offre, "cv": contenu_cv})
        response = llm.invoke(prompt)
        resultats.append({
            "nom": response.name,
            "note": response.note,
            "cv": contenu_cv  # Inclure le contenu du CV pour les questions d'entretien
        })
    return resultats

# Analyse des CVs
if 'offre' in locals() and 'contenus' in locals() and contenus:
    resultats_candidats = analyser_cvs(contenus, offre.content)

    st.subheader("Résultats de l'analyse des CVs")
    for resultat in resultats_candidats:
        st.write(f"**Nom :** {resultat['nom']}, **Note :** {resultat['note']}")
else:
    st.warning("Veuillez générer une offre et charger des CVs avant de procéder à l'analyse.")

# Affichage des scores des meilleurs candidats
def afficher_scores_top_candidats(resultats_candidats):
    no_candidat = st.slider('Nombre de candidats à représenter', 1, len(resultats_candidats))

    resultats_trier = sorted(resultats_candidats, key=lambda x: x['note'], reverse=True)[:no_candidat]

    noms = [resultat['nom'] for resultat in resultats_trier]
    notes = [resultat['note'] for resultat in resultats_trier]

    st.subheader("Représentation des scores")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(noms, notes, color="skyblue")
    ax.set_xlabel("Candidats", fontsize=14)
    ax.set_ylabel("Notes", fontsize=14)
    ax.set_title("Top candidats en fonction des notes des CV", fontsize=16)
    ax.set_ylim(0, 10)
    plt.xticks(rotation=45, ha="right", fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    st.pyplot(fig)
    return resultats_trier

# Classe pour générer les questions d'entretien
class QuestionsEntretien(BaseModel):
    nom: str = Field(description="Nom du candidat")
    questions: list[str] = Field(description="Liste des questions d'entretien")

questions_prompt = ChatPromptTemplate.from_template(
    """
    Génère des questions d'entretien personnalisées pour le candidat suivant en fonction de son CV et de l'offre :\n
    Offre :\n{offre}\n
    CV :\n{cv}\n
    Nom du candidat :\n{nom}\n
    Note :\n{note}\n
    Ne retourne que les informations définies dans la classe QuestionsEntretien.
    """
)

llm_questions = ChatGoogleGenerativeAI(temperature=0, model="gemini-2.0-flash").with_structured_output(QuestionsEntretien)

@st.cache_data
def generer_questions_entretien(resultats_trier, offre):
    questions_par_candidat = []
    for candidat in resultats_trier:
        prompt = questions_prompt.invoke({
            "nom": candidat['nom'],
            "note": candidat['note'],
            "cv": candidat['cv'],
            "offre": offre
        })
        response = llm_questions.invoke(prompt)
        questions_par_candidat.append({
            "nom": response.nom,
            "questions": response.questions
        })
    return questions_par_candidat

# Affichage des questions d'entretien
if 'resultats_candidats' in locals() and resultats_candidats:
    resultats_trier = afficher_scores_top_candidats(resultats_candidats)

    questions_entretien = generer_questions_entretien(resultats_trier, offre.content)

    st.subheader("Questions d'entretien personnalisées")
    for candidat_questions in questions_entretien:
        st.write(f"### Candidat : {candidat_questions['nom']}")
        for question in candidat_questions['questions']:
            st.write(f"- {question}")
        st.text_area(
            f"Réponses de {candidat_questions['nom']}:",
            placeholder=f"Écrire les réponses de {candidat_questions['nom']} ici..."
        )
else:
    st.warning("Veuillez analyser les CVs pour sélectionner des candidats et générer des questions d'entretien.")
