import streamlit as st
import os 
import matplotlib.pyplot as plt
from langchain_core.prompts import ChatPromptTemplate
from PyPDF2 import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field


os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

@st.cache_resource
def get_model():
    from langchain_google_genai import ChatGoogleGenerativeAI
    return ChatGoogleGenerativeAI(model="gemini-2.0-flash")
model = get_model()

st.title("📝 BEST-TALENT-AI")

besoins = st.text_area("Entrez vos besoins ici :", placeholder="Entrez votre texte...")

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
offre = generer_offre(besoins)


uploaded_files = st.file_uploader(
    "Choose a CV file", accept_multiple_files=True
)

contenus = {}
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    
    reader = PdfReader(uploaded_file)
    contenu = ""
    for page in reader.pages:
            contenu += page.extract_text() + "\n"
    contenus[uploaded_file.name] = contenu



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

resultats_candidats = None

@st.cache_data
def analyser_cvs(contenus, offre):
    resultats = []
    for nom_cv, contenu_cv in contenus.items():
        prompt = tagging_prompt.invoke({"offre": offre, "cv": contenu_cv})
        response = llm.invoke(prompt)
        resultats.append({
            "nom": response.name,
            "note": response.note
        })
    return resultats

if 'offre' in locals() and 'contenus' in locals() and contenus:
    resultats_candidats = analyser_cvs(contenus, offre.content)
    
    st.subheader("Résultats de l'analyse des CVs")
    for resultat in resultats_candidats:
        st.write(f"**Nom :** {resultat['nom']}, **Note :** {resultat['note']}")
else:
    st.warning("Veuillez générer une offre et charger des CVs avant de procéder à l'analyse.")


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

if resultats_candidats:
    x=afficher_scores_top_candidats(resultats_candidats)